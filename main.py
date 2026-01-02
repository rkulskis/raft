from communication.four_slot import FourSlot
from state.raft_server_state import RaftServerState, CLIENT_ID

import rclpy
from rclpy.node import Node
from std_msgs.msg import ByteMultiArray

import pickle
import re
import random
import argparse
import multiprocessing

class RaftServer(Node):
    def __init__(self, is_client=False):
        self.id = random.randint(1, 2 ** 31) if not is_client else CLIENT_ID
        node_name = f'RaftServer{self.id}'
        print(f"Creating {node_name}")
        super().__init__(node_name)

        # Create async raft topic with 1 slot. Subscribe to all raft peer topics
        self.publisher = self.create_publisher(ByteMultiArray, node_name, 1)
        self.inputs: dict[str, rclpy.subsctiption] = {}
        self.input_bufs: dict[str, FoutSlot] = {}
        self.state = RaftServerState(id=self.id)
        
        self.timer_poll = self.create_timer(1.0, self.subscribe_to_raft_servers)
        # loop at twice frequency of heartbeat, c.f. Nyquist frequency
        self.timer_raft = self.create_timer(50e-3, self.gather_compute_scatter)

    def read_input_msg(self, msg, id):
        data_dict = pickle.loads(b''.join(msg.data))
        
        if self.id not in data_dict: return
        
        my_data = data_dict[self.id]
        self.input_bufs[id].write(my_data)
        
    def subscribe_to_raft_servers(self):
        topics = self.get_topic_names_and_types()

        for topic_name, types in topics:
            if not topic_name.startswith('/RaftServer'): continue
            
            if topic_name in self.inputs: continue

            id = int(re.search(r"\d+", topic_name).group())
            if id == self.id: continue

            if id not in self.input_bufs:
                self.input_bufs[id] = FourSlot()

            self.inputs[topic_name] = self.create_subscription(
                ByteMultiArray,
                topic_name,
                lambda msg, id=id: self.read_input_msg(msg, id),
                1
            )

    def state_add_raft_server(id):                
        if id == CLIENT_ID: continue
        
        self.state.volatile_leader.match_index[id] = self.state.prev_log_index
        self.state.volatile_leader.next_index[id] = self.state.prev_log_index
        self.state.raft_cardinality += 1
            
    def gather_compute_scatter(self):
        in_msgs = {}
        for in_id, in_buf in list(self.input_bufs.items()):
            if in_id not in self.state.volatile_leader.match_index:
                # Accesses shared state so must do in serialized execution
                self.add_raft_server_to_state(id)
                
            in_msgs[in_id] = in_buf.read()
            if in_msgs[in_id] is None: continue
            
            if self.id != CLIENT_ID: print(f'{self.id} Got: {in_msgs[in_id]}')
            
            self.state.recv(in_msgs[in_id], in_id)

        self.state.compute()

        out_msgs = {}

        for id, in_msg in in_msgs.items():
            out_msgs[id] = self.state.send(in_msg, id)
            if out_msgs[id] is not None and self.id != CLIENT_ID:
                print(f'Sent {out_msgs[id]} to {id}')

        batch_msg = ByteMultiArray()
        serialized = pickle.dumps(out_msgs, protocol=pickle.HIGHEST_PROTOCOL)
        batch_msg.data = serialized
        self.publisher.publish(batch_msg)

def run_raft_server(is_client=False):
    """Run a single RaftServer instance"""
    rclpy.init()
    raft_server = RaftServer(is_client)
    try:
        rclpy.spin(raft_server)
    finally:
        raft_server.destroy_node()
        rclpy.shutdown()

def main(num_servers, is_client):
    processes = []
    
    for i in range(num_servers):
        p = multiprocessing.Process(
            target=run_raft_server,
            kwargs={'is_client': is_client}
        )
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

    num_servers = 1 if args.client else 5
    main(num_servers, is_client=args.client)
