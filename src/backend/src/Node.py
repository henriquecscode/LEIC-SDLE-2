import kademlia
from Connection import Connection
from Info import Info
from kademlia.network import Server
from kademlia.routing import RoutingTable
import asyncio
import logging
import threading
import json

import time
from datetime import datetime



class Node:

    BASE_PORT = 8468
    BASE_HOST = '127.0.0.1'

    def __init__(self, id, peer):
        self.server = Server()
        
        self.peer = peer
        self.host = self.BASE_HOST
        self.node_port = self.BASE_PORT + id   
      
    def logs():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

    def run_in_loop(self, function, loop):
        return loop.run_until_complete(function)

    def start(self): # connect to other nodes

        #Need to separate the bootstrapping from the user functions
        print("Starting node...")
        self.server = Server()
        self.loop = asyncio.new_event_loop()
        self.b_nodes = [(self.BASE_HOST, self.BASE_PORT)]
        print("Bootstrap nodes: ", self.b_nodes)
        self.loop.run_until_complete(self.server.listen(self.node_port))
        print("Listening on port: ", self.node_port)
        self.loop.run_until_complete(self.server.bootstrap(self.b_nodes))
        print("Bootstrapped")

        # Start server
        self.connection = Connection(self.BASE_HOST, self.node_port, self.peer.handler)
        self.connection.bind()
        self.listener_thread = threading.Thread(target=self.connection.listen)
        self.listener_thread.start()
        self.loop.run_forever()
    

    def send_message_from_info(self, info, message):
        if info.is_online:
            connection = Connection(info.ip, info.port, lambda x: None)
            connection.connect()
            connection.send(message)
        else:
            print(f"User {info.username} is not online")
    def send_message(self, key, message):
        print("SENDING MESSAGE")
        info = self[key]
        self.send_message_from_info(info, message)

    def get(self, key):
        val = self.server.get(key)
        return val
        
    def __getitem__(self, key):
        try:
            info = asyncio.run_coroutine_threadsafe(self.get(key), self.loop)
            info = info.result()
            if info is None:
                return None
            return Info.deserialize(info)
        except Exception as e:
            print("Exception getting cloud info: ", e)
            return None

    def __setitem__(self, key, value: Info):
        try: 
            asyncio.run_coroutine_threadsafe(self.set(key, value.serialize()), self.loop)
        except Exception as e:
            print("Exception setting cloud info", e)
            pass

    async def set(self, key, value):
        val = await self.server.set(key, value)
        return val

### INFO HANDLING ###

    def add_follow(self, follower, following):
        print("Adding follow", follower, following)
        to_add_following = True
        to_add_follower = True

        if follower == self.peer.username:
            self.add_following(following)
            follower_info = self.peer.info
            to_add_following = False
        elif following == self.peer.username:
            self.add_follower(follower)
            to_add_follower = False
            following_info = self.peer.info
            
        if to_add_following:
            follower_info = self.get_info(follower)
            if follower_info is not None:
                follower_info = follower_info.add_following(following)
                self[follower] = follower_info
            else:
                print("Follower info is none in Node's add_follow")
        if to_add_follower:
            following_info = self.get_info(following)
            if following_info is not None:
                following_info = following_info.add_follower(follower)
                self[following] = following_info
            else:
                print("Following info is none in Node's add_follow")

        return (follower_info, following_info)
    
    def remove_follow(self, follower, following):
        print("Removing follow", follower, following)
        to_remove_following = True
        to_remove_follower = True

        if follower == self.peer.username:
            self.remove_following(following)
            follower_info = self.peer.info
            to_remove_following = False
        elif following == self.peer.username:
            self.remove_follower(follower)
            to_remove_follower = False
            following_info = self.peer.info

        if to_remove_following:
            follower_info = self.get_info(follower)
            if follower_info is not None:
                follower_info = follower_info.remove_following(following)
                self[follower] = follower_info
            else:
                print("Follower info is none in Node's remove_follow")

        if to_remove_follower:
            following_info = self.get_info(following)
            if following_info is not None:
                following_info = following_info.remove_follower(follower)
                self[following] = following_info
            else:
                print("Following info is none in Node's remove_follow")

        return (follower_info, following_info)

    def add_follower(self, follower):
        self.peer.info.add_follower(follower)
        self.set_info()
        return self

    def remove_follower(self, follower):
        self.peer.info.remove_follower(follower)
        self.set_info()
        return self

    def add_following(self, following):
        self.peer.info.add_following(following)
        self.set_info()
        return self

    def remove_following(self, following):
        self.peer.info.remove_following(following)
        self.set_info()
        return self

    def set_info(self):
        self.peer.info.ip = self.host
        self.peer.info.port = self.node_port
        self[self.peer.username] = self.peer.info
        return self

    def get_info(self, username) -> Info:
        return self[username]

### LIFETIME ###
def stop(self):
    ### Terminate protocols and spread information and whatnot (maybe at an higher level?)
    self.server.stop()
    self.listener_thread.join()
    self.loop.close()

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()