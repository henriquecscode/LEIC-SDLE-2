import sys
from Backend import Backend
from Peer import Peer

IP = '127.0.0.1'


def args():
    if len(sys.argv) != 2:
        raise Exception("Must have an integer <id> argument")
    id = int(sys.argv[1])

    if id < 0:
        raise Exception("<id> argument must be greater than 0")

    return int(id)

if __name__ == "__main__":

    id = args()
    peer = Peer(id)
    backend = Backend(peer)
    backend.start()
    peer.add_backend(backend)
    peer.start()