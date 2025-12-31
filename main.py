import rclpy
from rclpy.node import Node

from std_msgs.msg import ByteMultiArray
import pickle

import re
import random
import argparse

from communication.four_slot import FourSlot
from state.raft_server_state import RaftServerState, CLIENT_ID

class RaftServer(Node):
    def __init__(self, is_client=False):
        self.id = random.randint(1, 2 ** 31) if not is_client else CLIENT_ID
        node_name = f'RaftServer{self.id}'
        print(f"Creating {node_name}")
        super().__init__(node_name)

        # Create async raft topic with 1 slot. Subscribe to all raft peer topics
        self.publisher = self.create_publisher(ByteMultiArray, node_name, 1)
        self.inputs = {}  # topic_name -> subscription
        self.input_bufs = {}
        self.timer_poll = self.create_timer(1.0, self.scan_topics)

        # Loop at twice frequency of heartbeat, c.f. Nyquist frequency
        half_heartbeat_timeout = 50e-3
        self.timer_raft = self.create_timer(half_heartbeat_timeout, self.loop)
        
        self.state = RaftServerState(id=self.id)

    def input_callback(self, msg, id):
        data_dict = pickle.loads(b''.join(msg.data))
        
        if self.id not in data_dict:
            return
        
        data = data_dict[self.id]

        # print(f'self.state = {self.state}')
        self.input_bufs[id].write(data)
        
    def scan_topics(self):
        topics = self.get_topic_names_and_types()

        for topic_name, types in topics:
            if not topic_name.startswith('/RaftServer'):
                continue

            if topic_name in self.inputs:
                continue

            id = int(re.search(r"\d+", topic_name).group())

            if id == self.id:
                continue

            self.get_logger().info(f"Subscribing to {topic_name}")
            
            if id not in self.input_bufs:
                self.input_bufs[id] = FourSlot()
                
            sub = self.create_subscription(
                ByteMultiArray,
                topic_name,
                lambda msg, id=id: self.input_callback(msg, id),
                1
            )

            self.inputs[topic_name] = sub        

    def loop(self):
        in_msgs = {}
        for in_id, in_buf in list(self.input_bufs.items()):
            in_msgs[in_id] = in_buf.read()
            if in_id not in self.state.volatile_leader.match_index and \
               in_id != CLIENT_ID:
                self.state.volatile_leader.match_index[in_id] = self.state.prev_log_index
                self.state.volatile_leader.next_index[in_id] = self.state.prev_log_index
                self.state.raft_cardinality += 1

            if not in_msgs[in_id]:
                continue

            if self.id != CLIENT_ID:
                print(f'{self.id} Got: {in_msgs[in_id]}')
            self.state.recv(in_msgs[in_id], in_id)

        self.state.tick()

        out_msgs = {}

        for id, in_msg in in_msgs.items():
            out_msg = self.state.send(in_msg, id)
            if out_msg is not None and self.id != CLIENT_ID:
                print(f'Sent {out_msg} to {id}')            
            out_msgs[id] = out_msg

        # Batch as one message, then subscribers filter by their id
        msg = ByteMultiArray()
        serialized = pickle.dumps(out_msgs, protocol=pickle.HIGHEST_PROTOCOL)
        msg.data = serialized
        self.publisher.publish(msg)

import multiprocessing

def run_raft_server(is_client=False):
    """Run a single RaftServer instance"""
    rclpy.init()
    raft_server = RaftServer(is_client)
    try:
        rclpy.spin(raft_server)
    finally:
        raft_server.destroy_node()
        rclpy.shutdown()

def main(is_client):
    num_servers = 5 if not is_client else 1
    processes = []
    
    for i in range(num_servers):
        kwargs = {'is_client': is_client} if i == 0 else {}
        p = multiprocessing.Process(target=run_raft_server, kwargs=kwargs)
        p.start()
        processes.append(p)
        print(f"Started RaftServer process {i+1}/{num_servers} (PID: {p.pid})")
    
    # Wait for all processes to complete (or Ctrl+C)
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\nShutting down all RaftServers...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client',
        action='store_true',
        help='Run in client mode'
    )
    args = parser.parse_args()

    main(is_client=args.client)
