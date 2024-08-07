import socket
import json
from Message import Message, MessageDecodeError
import threading

BUFFER_SIZE = 1024
class Connection:
    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = handler
    
    def bind(self):
        print("Binding to", self.host, self.port)
        self.socket.bind((self.host, self.port))

    def connect(self):
        connected = False

        while not connected:
            try:
                print("Connecting to", self.host, self.port)
                self.socket.connect((self.host, self.port))
                print("Connected to", self.host, self.port)
                connected = True
            except Exception as e: 
                print("error in connect:", e)
    
    def listen(self):
        print("Connection server on port: ", self.port)
        try:
            self.socket.listen()

            while True:
                user_socket, user_address = self.socket.accept()
                print("Connection from", user_address, "has been established!")
                while True:
                    packet = user_socket.recv(BUFFER_SIZE).decode("utf-8")
                    print('Received a packet', packet)
                    # break
                    try:
                        message = Message.deserialize(packet)
                        threading.Thread(target=self.handler, args=(message,)).start()
                        break
                    except json.JSONDecodeError:
                        print(f"I had an oopsie with JSON\n{packet}")
                        continue
                    except MessageDecodeError:
                        print(f"I had an oopsie with Message\n{packet}")
                        continue
                    except Exception as e:
                        print("error in listen:", e)
                        break

        except Exception as e:
            print("error in listen:", e)
       
    
    def send(self, message):
        try:
            self.socket.send(bytes(message, encoding="utf-8"))
        except Exception as e:
            print("error in send:", e)
        finally:
            self.close()

    def close(self):
        self.socket.close()
