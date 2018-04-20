#!/usr/bin/python3
import argparse

import xmlrpc.client


def probe_node(address, port):
    """
        This is an information gathering function. It calls the getBusInfo function and parses all the info into a more usable form 
    """

    ID = '/rosnode'
    topicList = []
    with xmlrpc.client.ServerProxy("http://" + address + ":" + port) as proxy:
        topicInfo = proxy.getBusInfo(ID)
        nodeName = proxy.getName(ID)
        if topicInfo[0] == 1 and nodeName[0] == 1:
            print("Successfully got the bus info")
            print(nodeName[2])
            for topic in topicInfo[2]:
                print(topic)
                topicList.append(topic[4])
                print(topic[4])
            return (nodeName[2], topicList, topicInfo[2])
        else:
            print("Got an error message with the command. " + topicInfo[1] + topicInfo[2])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get the information about a given node (Name/Topics publisher of/Topics subscriber to)')
    parser.add_argument('-a', '--address', help="Address of the ROS node you want info on", required=True)
    parser.add_argument('-p', '--port', help="Port of the ROS node you want info on", required=True)
    args = parser.parse_args()
    nodeInfo = probe_node(args.address, args.port)
    print(nodeInfo)
