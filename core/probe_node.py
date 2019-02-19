#!/usr/bin/python3
import argparse
import xmlrpc.client

from core.node import Node


def probe_node(node: Node):
    """
        This is an information gathering function. It calls the getBusInfo function and parses all the info
         into a more usable form
    """

    node_id = '/rosnode'
    topic_list = []
    with xmlrpc.client.ServerProxy("http://" + node.ip_addr + ":" + node.port) as proxy:
        topic_info = proxy.getBusInfo(node_id)
        node_name = proxy.getName(node_id)
        if topic_info[0] == 1 and node_name[0] == 1:
            print("Successfully got the bus info")
            print(node_name[2])
            for topic in topic_info[2]:
                print(topic)
                topic_list.append(topic[4])
                print(topic[4])
            return node_name[2], topic_list, topic_info[2]
        else:
            print("Got an error message with the command. " + topic_info[1] + topic_info[2])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get the information about a given node (Name/Topics publisher of/Topics subscriber to)')
    parser.add_argument('-a', '--address', help="Address of the ROS node you want info on", required=True)
    parser.add_argument('-p', '--port', help="Port of the ROS node you want info on", required=True)
    args = parser.parse_args()
    cur_node = Node(ip_addr=args.address, port=args.port)
    nodeInfo = probe_node(cur_node)
    print(nodeInfo)
