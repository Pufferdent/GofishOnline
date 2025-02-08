from lib import *
from gui import *
from socketHelper import *
import random
import time
import json
import os


#Better interaction with gui:

def getVal():
    with open("val.json") as file:
        return json.load(file)

#------------------------------------------------------------
#
#     This part is responsible for creating accounts and logging in.
#
#------------------------------------------------------------

if not os.path.exists('account.json'):
    with open('account.json', "w") as file:
        ""

#Load login data
with open('account.json', 'r') as file:
    accountData = file.read()

def register():
    gui.gui.print("Please create an account.")
    name = gui.gui.input("Enter your name: ")
    random.seed(name + str(time.time())) #automatically randomly generate a password
    password = ""
    for _ in range(20):
        password += chr(random.randint(0, 25)+97)

    #Request new account
    response = getRequest("/NEWACC " + name + " " + password)

    if response == "SUCCESS! Created new account.":
        accountInfo = {"name": name, "password": password}
        with open('account.json', 'w') as file:
            json.dump(accountInfo, file, indent=4)

        return name, password
    else:
        gui.gui.print("Failed to create account!")
        gui.gui.print(response)
        return register()

if accountData.strip() == '':#If no account
    username, password = register()

else:#Already existing account
    account = json.loads(accountData)
    username = account["name"]
    password = account["password"]



#------------------------------------------------------------
#
#     This part is responsible for handling tokens. Resuming & creating new tokens.
#
#------------------------------------------------------------

with open('token.json', 'r') as file:#Finding if token exists
    tokenData = file.read()

if accountData.strip() != '': #If existing token (resuming a game):
    tokenInfo = json.loads(tokenData)
    if username == tokenInfo["name"]:
        token = tokenInfo["token"]

    response = getRequest("/RESUME " + token)

    if response[:6] == "ERROR:":
        gui.gui.error(response)
        raise Exception("Resume failed! " + response)
    
    if response[:8] == "SUCCESS!":
        gui.gui.print("Resumed game.")

        gameInfo = json.loads(response[8:])


else: #If no existing token (new game):
    response = getRequest("/LOGIN " + username + " " + password)

    if response[:6] == "ERROR:":
        gui.gui.error(response)
        raise ValueError("Could not login. " + response)

    token = response[len("SUCCESS! Logged in. Token: "):]

    tokenInfo = {"name": username, "token" : token}
    with open('token.json', "w") as file:
        json.dump(tokenInfo, file, indent=4)

#------------------------------------------------------------
#
#     After creating a new token, the system should queue into a game. It will automatically queue, and you can change the queue code.
#
#------------------------------------------------------------

    queueCode = gui.gui.input("Enter your queue code: ")
    if queueCode == "":
        queueCode = "default4"

    response = getRequest("/QUEUE " + token + " " + queueCode)

    gui.gui.print(response)

    while True:
        response = getRequest("/QUEUEINFO " + token)
        if response[:29] == "SUCCESS! Still queueing with ":
            gui.gui.print(response)
        if response == "SUCCESS! Queued a game.":
            break
        val = getVal()
        if "newQueueCode" in val:
            queueCode = val["newQueueCode"]
            response = getRequest("/QUEUE " + token + " " + queueCode)
        time.sleep(0.5)
    response = getRequest("/RESUME " + token)

#------------------------------------------------------------
#
#     Main game loop starts here
#
#------------------------------------------------------------


while True:
    response = getRequest("/GAMEINFO " + token)
    if response == "Connection Failed!":
        gui.gui.print("Connection Failed, restarting soon...")
        time.sleep(1)
    else:
        #Game data...
        
        #Render game data

        #If my turn, play

        #if not, wait
        pass