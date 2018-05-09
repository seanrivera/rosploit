import os

import nmap

from demo import demo
from rosploit.node import Node

# TODO: THIS IS BAD. JUST HERE TO MAKE IT WORK
NMAP_DATA_DIR = os.path.join(demo.root_path, "..", "rosploit_scan")


def scan_node(ip_addr: str, port_range: str, script_list: str) -> str:
    nm = nmap.PortScanner()
    print("Starting scan ip addr " + ip_addr + " ports " + port_range)
    print(NMAP_DATA_DIR)
    argline = '--datadir=' + NMAP_DATA_DIR
    print(argline)
    # nm.scan(hosts=ip_addr, ports=port_range, arguments=argline + ' -sV --script="' + script_list + '"')
    nm.scan(hosts=ip_addr, ports=port_range, arguments='-sV')
    print(nm.command_line())
    print(nm.scaninfo())
    print(nm.all_hosts())
    if 'up' not in nm[ip_addr].state():
        print(nm[ip_addr].state())
        print("IP addr not up " + ip_addr)
        raise Exception('Node Down')
    elif 'tcp' not in nm[ip_addr].all_protocols():
        print("No open tcp ports in " + port_range)
        raise Exception("No TCP ports")
    node_list = []
    lport = sorted(nm[ip_addr]['tcp'].keys())
    print(lport)
    for port in lport:
        # TODO: Just the ROS ports
        print(port)
        try:
            tempnode = Node(ip_addr=ip_addr, port=port)
        except Exception as inst:
            print("Node Creation Exception")
            raise inst
        node_list.append(tempnode)
    return node_list


if __name__ == "__main__":
    scan_node('127.0.0.1', '1-')
