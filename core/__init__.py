from .node import Node
from .probe_node import probe_node

node_scripts = ['kill_node', 'probe_node']
service_scripts = []
topic_scripts = []
node_name = "/rosploit"
__all__ = node_scripts + service_scripts + topic_scripts
