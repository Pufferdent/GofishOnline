
import socket
from datetime import datetime
from main import *

# Define the server address and port
HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 45246        # Port to listen on (non-privileged ports are > 1023)

def log(addr, data):
    with open("logs.txt", "a") as file:
        file.write(str(addr) + ": " + data + "\n")

cdTracker = {}

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the address and port
    s.bind((HOST, PORT))
    # Enable the server to accept connections
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        # Wait for a connection
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                decoded_data = data.decode('utf-8')  



                request = decoded_data.split()
                response = "Not a valid command!"

                if decoded_data != "/tfpljrxtrjhwapsfqqjj":
                    print(f"Connected by {addr}")
                    print(decoded_data)
                    log(addr, decoded_data)

                if cdTracker.get(addr[0]) is not None:
                    cdTracker[addr[0]] = max(cdTracker[addr[0]]+0.5, time.time()-5)
                else:
                    cdTracker[addr[0]] = time.time()-5
                if cdTracker[addr[0]] > time.time():
                    response = "Don't spam!"

                if response != "Don't Spam!":
                    #These commands are NOT formatted-- they do not require a username and a token like all other commands.
                    if request[0] in ["/NEWACC", "/LOGIN", "/TEST", "/tfpljrxtrjhwapsfqqjj"]:
                        try:
                            if request[0] == "/NEWACC":
                                response = main.newAccount(request[1], request[2], addr[0]) #request[1] is name, request[2] is password
                            if request[0] == "/LOGIN":
                                response = main.login(request[1], request[2]) #request[1] is name, request[2] is password
                            if request[0] == "/TEST":
                                response = "Recived test message! You are " + str(addr)
                            if request[0] == "/tfpljrxtrjhwapsfqqjj":
                                response = main.selfRefresh()
                        except IndexError:
                            response = "ERROR: Incorrect Command!"
                
                
                    else: #These commands ARE formatted-- checking token before everything.
                        try:
                            token = request[1]
                            name = main.verifyToken(token)
                            if name != "<Failed>":
                                """
                                if request[0] == "/GETSTATUS":
                                    response = main.getStatus()
                                if request[0] == "/QUEUEGAME":
                                    response = main.queue(token, name, request[2])
                                if request[0] == "/QUEUEINFO":
                                    response = main.queueInfo(token)
                                if request[0] == "/GAMEINFO":
                                    response = main.gameInfo(token)
                                if request[0] == "/ASKCARD":
                                    response = main.askCard(token, request[1], request[2])
                                """
                                if request[0] == "/MAINGAME":
                                    if request[2] == "JOIN":
                                        response = main.joinRoom(token, name, request[3])
                                    if request[2] == "NEWROOM":
                                        response = main.newRoom(token, name)
                                    if request[2] == "LEAVEROOM":
                                        response = main.leaveRoom(token, name)
                                    if request[2] == "INFO":
                                        response = main.gameInfo(token, name)
                                    if request[2] == "START":
                                        response = main.startGame(token, name)
                                    if request[2] == "ASK":
                                        response = main.askCard(token, name, request[3], request[4])
                                        #(token, name, target, card)
                                    if request[2] == "DECLARE":
                                        response = main.declare(token, name, request[3])
                                        #request[3] should contain all data for the declaration.
                                        #First digit: Group of card.
                                        #2-7th digit: Who has that certain card.
                                        
                            else:
                                response = "ERROR: Invalid Token!"
                                
                        except IndexError:
                            response = "ERROR: Incorrect Command!"

                if decoded_data != "/tfpljrxtrjhwapsfqqjj":
                    print(response)
                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    log(formatted_time, response)
                
                if conn:
                    conn.sendall((decoded_data + " " + response).encode())
