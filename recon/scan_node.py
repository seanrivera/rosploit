import os
from typing import List

import nmap

# from demo import demo
from core.node import Node

# TODO: THIS IS BAD. JUST HERE TO MAKE IT WORK
# NMAP_DATA_DIR = os.path.join(demo.root_path, "..", "rosploit_recon")


# NMAP_DATA_DIR = demo.root_path + "\\\\"+".." + "\\\\" + "rosploit_recon"
NMAP_DATA_DIR = os.path.dirname(os.path.realpath(__file__))


def scan_host(ip_addr: str, port_range: str, script_list: List[str]) -> List[Node]:
    """
    Scan all of the ROS nodes for a given ip address and port range. Wraps nmap
    :param ip_addr: IP address to scan
    :param port_range: Port range to scan over
    :param script_list: List of NSE scripts to execute.
    :return:
    """
    nm = nmap.PortScanner()
    print("Starting scan ip addr " + ip_addr + " ports " + port_range)
    DATA_DIR = NMAP_DATA_DIR.replace("\\", '\\\\')
    scripts = ""
    new_list = [os.path.join(DATA_DIR, s) for s in script_list]
    scripts = ",".join(new_list)

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
    #  print(nm[ip_addr].state())
    #   print(nm[ip_addr].all_protocols())
    node_list = []
    lport = sorted(nm[ip_addr]['tcp'].keys())
    #    print(lport)
    for port in lport:
        # TODO: Just the ROS ports
        # print(port)
        try:
            # print(nm[ip_addr]['tcp'][port])
            # print(nm[ip_addr]['tcp'][port]['extrainfo'])
            notes = nm[ip_addr]['tcp'][port]['extrainfo'] + ' '
            if 'script' in nm[ip_addr]['tcp'][port] and 'ros-node-id' in nm[ip_addr]['tcp'][port]['script']:
                if nm[ip_addr]['tcp'][port]['script']['ros-node-id'] and not "ERROR:" in \
                                                                             nm[ip_addr]['tcp'][port]['script'][
                                                                                 'ros-node-id']:
                    for key, value in nm[ip_addr]['tcp'][port]['script'].items():
                        notes = notes + key + ":" + value + "\n"
                    temp_node = Node(ip_addr=str(ip_addr), port=str(port), notes=notes)
                    node_list.append(temp_node)
                    # print(temp_node.notes)
        except Exception as inst:
            print("Node Creation Exception")
            raise inst
    return node_list


if __name__ == "__main__":
    results = scan_host('127.0.0.1', '1-', ['ros-master-scan.nse', 'ros-node-id.nse'])
    for node in results:
        print(node.port)
        print(node.notes)
        if "Publisher" in node.notes:
            node.get_pub_list("/id")
            node.get_sub_list("/id")
            for pub in node.pub_topics:
                print(pub.name)
                print(pub.md5_sum)
            for sub in node.sub_topics:
                print(sub.name)
                print(sub.md5_sum)
