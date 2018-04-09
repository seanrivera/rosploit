#!/usr/bin/python3
import argparse


def reset_node(address, port):
    print("TODO")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reset a given ROS node')
    parser.add_argument('-a', '--address', help="Address of the ROS node you want to reset", required=True)
    parser.add_argument('-p', '--port', help="Port of the ROS node you want to reset", required=True)
    args = parser.parse_args()
    reset_node(args.address, args.port)
