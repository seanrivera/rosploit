import signal
import sys

import recon


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


def print_options():
    print("Welcome to rosploit")
    print("Enter a number to activate that option")
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


def scan_system():
    return recon.scan_host('127.0.0.1', '1-', ['ros-master-scan.nse', 'ros-node-id.nse'])


def print_graph():
    print("TODO")


def kill_node():
    print("TODO")


def dos():
    print("TODO")


def port_exhaust():
    print("TODO")


def list_param():
    print("TODO")


def change_param():
    print("TODO")


def data_inject():
    print("TODO")


def replace_node():
    print("TODO")


def mitm():
    print("TODO")


def rosploit():
    signal.signal(signal.SIGINT, signal_handler)
    function_list = [scan_system, print_graph, kill_node, dos, port_exhaust, list_param, change_param, data_inject,
                     replace_node,
                     mitm]
    while (True):
        print_options()
        option = int(input("Select option:"))
        if option > len(function_list):
            print(option) 
            print("Invalid Option")
        else:
            function_list[option - 1]()

if __name__ == "__main__":
    rosploit()
