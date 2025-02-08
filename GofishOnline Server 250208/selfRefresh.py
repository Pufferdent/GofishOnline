import socket
import time

HOST = '49.232.238.132'  # The server's hostname or IP address
PORT = 45246        # The port used by the server

def getRequest(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(message.encode())
            data = s.recv(4096)
        
            print("SENT:" + message)
            print("RECIEVED: " + str(data[len(message)+1:])[2:-1])
        except ConnectionRefusedError:
            print("Connection Refused! The server is probably down.")
    
    return str(data[len(message)+1:])[2:-1]

if __name__ == '__main__':
    while True:
        try:
            print(getRequest("/tfpljrxtrjhwapsfqqjj"))
        except:
            pass
        time.sleep(2)