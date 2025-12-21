import rclpy
from rclpy.node import Node

from std_msgs.msg import ByteMultiArray
import pickle

import re
import random

from communication.four_slot import FourSlot
from state.raft_server_state import RaftServerState

class RaftServer(Node):
    def __init__(self):
        self.id = random.randint(1, 2 ** 31)
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
        
        self.state = RaftServerState(self.id)

    def input_callback(self, msg, topic_name):
        id = int(re.search(r"\d+", topic_name).group())

        data = pickle.loads(bytes(msg.data))[self.id]

        if id not in self.input_bufs:
            self.input_bufs[id] = FourSlot()
            
        self.input_bufs[id].write(data)
        
    def scan_topics(self):
        topics = self.get_topic_names_and_types()

        for topic_name, types in topics:
            if not topic_name.startswith('RaftServer'):
                continue

            if topic_name in self.inputs:
                continue

            msg_type = self.resolve_type(types[0])
            self.get_logger().info(f"Subscribing to {topic_name}")

            sub = self.create_subscription(
                msg_type,
                topic_name,
                lambda msg, t=topic_name: self.input_callback(msg, t),
                1
            )

            self.inputs[topic_name] = sub        

    def loop(self):
        in_msgs = {}
        for in_id, in_buf in list(self.input_bufs.items()):
            in_msgs[in_id] = in_buf.read()
            self.state.recv(in_msgs[in_id], in_id)

        self.state.tick()

        out_msgs = {}
        
        for id, in_msg in self.in_msgs.items():
            out_msg = self.state.send(in_msg, id)
            out_msgs[id] = out_msg

        # Batch as one message, then subscribers filter by their id
        msg = ByteMultiArray()
        msg.data = list(pickle.dumps(out_msgs))
        self.publisher.publish(msg)

def main():
    rclpy.init()

    raft_server = RaftServer()

    rclpy.spin(raft_server)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    raft_server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
