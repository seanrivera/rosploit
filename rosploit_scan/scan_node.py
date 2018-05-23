import os
from typing import List

import nmap

from demo import demo
from rosploit.node import Node

# TODO: THIS IS BAD. JUST HERE TO MAKE IT WORK
NMAP_DATA_DIR = os.path.join(demo.root_path, "..", "rosploit_scan")


# NMAP_DATA_DIR = demo.root_path + "\\\\"+".." + "\\\\" + "rosploit_scan"

def scan_node(ip_addr: str, port_range: str, script_list: List[str]) -> List[Node]:
    nm = nmap.PortScanner()
    print("Starting scan ip addr " + ip_addr + " ports " + port_range)
    print(NMAP_DATA_DIR)
    DATA_DIR = NMAP_DATA_DIR.replace("\\", '\\\\')
    print(DATA_DIR)
    scripts = ""

    new_list = [DATA_DIR + "\\\\" + s for s in script_list]
    print(new_list)
    scripts = ",".join(new_list)
    print(scripts)

    try:
        nm.scan(hosts=ip_addr, ports=port_range, arguments='-sV --script=' + scripts)
    except Exception as inst:
        print("Exception type " + str(type(inst)))
        print("Failed to scan node because " + str(inst))
        raise inst
    print(nm.command_line())
    print(nm.scaninfo())
    print(nm.all_hosts())

    try:
        if 'up' not in nm[ip_addr].state():
            print(nm[ip_addr].state())
            print("IP addr not up " + ip_addr)
            raise Exception('Node Down')
        elif 'tcp' not in nm[ip_addr].all_protocols():
            print("No open tcp ports in " + port_range)
            raise Exception("No TCP ports")
    except Exception as inst:
        print("Exception type " + str(type(inst)))
        print("Failed to check node info because " + str(inst))
        raise inst
    print(nm[ip_addr].state())
    print(nm[ip_addr].all_protocols())
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
    results = scan_node('127.0.0.1', '1-')
