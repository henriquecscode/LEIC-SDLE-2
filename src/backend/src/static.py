import asyncio
import logging
import sys
from threading import Thread
from kademlia.network import Server



class Bootstrap(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.set_logger()
        self.server = Server()
        self.ip = ip
        self.port = port

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.server.listen(self.port))
        asyncio.run(self.server.set('test', 'test'))
        try:
            print(f"[Started] Bootstrap on ip {self.ip} and port {self.port}")
            loop.run_forever()
        except KeyboardInterrupt:
            print(f"[Stopped] Bootstrap on ip {self.ip} and port {self.port}")
        finally:
            loop.stop()

    def set_logger(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)


if __name__ == '__main__':
    Bootstrap('127.0.0.1', 8468).start()
