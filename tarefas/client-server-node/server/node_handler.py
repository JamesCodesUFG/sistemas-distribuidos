import socket

import threading

class NodeHandler(threading.Thread): 
    __node_pool: list = []

    def __init__(self):
        pass

    def run(self):
        

