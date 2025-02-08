import json
import time
import random
import os
import csv
import lib

IDLE = 360000 #time for idle

class main:
    def invalidName(name):
        if len(name) < 4 or len(name) > 32:
            return True
        for char in name:
            if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-":
                return True
        return False
    
    def locateGame(token, name):
        with open("existingGames.json", "r") as file:
            existingGames = json.load(file)
        if existingGames == None:
            existingGames = {}
        flag = True
        for loopgameID, loopplayers in existingGames.items():
            for item in loopplayers:
                if item["token"] == token and item["name"] == name:
                    gameID = loopgameID
                    players = loopplayers
                    flag = False
        if flag:
            return existingGames, "<none>", []
        if os.path.exists("existingGames/" + gameID + ".json"):
            with open("existingGames/"+gameID + ".json", "r") as file:
                return json.load(file), gameID, players
        else:
            return {}, gameID, players



    def newAccount(name, password, ip):
        if main.invalidName(name):
            return "ERROR: Invalid name!"
        with open('accounts.json', 'r') as file:
            accountData = json.load(file)
            for account in accountData:
                if account["name"] == name:
                    return "ERROR: Existing name."

        account = {"name": name, "password": password, "creationIP": ip}
        accountData.append(account)

        with open('accounts.json', 'w') as file: #Append the new account into the system
            json.dump(accountData, file, indent=4)
        return "SUCCESS! Created new account."
    
    def login(name, password):
        

        with open('accounts.json', 'r') as file:
            accountData = json.load(file)
        for account in accountData:
            if account["name"] == name:
                if account["password"] == password:
                    random.seed(name + password + str(time.time()))
                    with open('existingTokens.csv', "r") as file:
                        allTokens = file.read().split("\n")
                        for line in allTokens:
                            if name == line.split(",")[0]:
                                return line.split(",")[1]
                    token = ""
                    for _ in range(32):
                        token += chr(random.randint(0, 25)+97)
                    with open('existingTokens.csv', 'a') as file:
                        file.write(name + "," + token + "," + str(time.time()) + "\n")
                    return token
                else:
                    return "ERROR: Incorrect password."
        return "ERROR: Account not found."
    
    def verifyToken(token):
        with open('existingTokens.csv', "r") as file:
            allTokens = file.read()
        for line in allTokens.split("\n"):
            f = line.split(",")
            if token == f[1]:
                return f [0]
        return "<Failed>"

    """
    def getStatus():
        with open('existingTokens.csv', "r") as file:
            allTokens = file.read()
        players = len(allTokens)
        files = os.listdir('/existingGames')
        # Filter the list to include only files
        files = [file for file in files if os.path.isfile(os.path.join('/existingGames', file))]
        games = len(files)
        return f"SUCCESS! Current Players: {players} Current Games: {games}"

    def queue(token, name, queueCode = "default"):
        with open("queue.json", "r") as file:
            curQueue = json.load(file)
        for player in curQueue:
            if player["token"] == token:
                curQueue["code"] = queueCode
                with open("queue.json", "w") as file:
                    file.write(curQueue)
                return "SUCCESS! Requeued using code " + queueCode
        player = {"token": token, "code" : queueCode, "player": name}
        curQueue.append(player)
        with open("queue.json", "w") as file:
            file.write(curQueue)
        return "SUCCESS! Queued using code " + queueCode
    
    def queueInfo(token):
        with open("queue.json", "r") as file:
            curQueue = json.load(file)
        for item in curQueue:
            if item["token"] == token:
                code = item["code"]
        player = 0
        for item in curQueue:
            if item["code"] == code:
                player += 1
        return "SUCCESS! Still in queue with " + player + " players."

    def selfRefresh():
        #-----Checking queue
        with open("queue.json", "r") as file:
            curQueue = json.load(file)
        with open("existingGames.json", "r") as file:
            existingGames = json.load(file)
        oldQueue = curQueue
        players = {}
        for item in oldQueue:
            players[item["code"]].append(item)
            playerAmount = int(item["code"][-1], base=10)
            if playerAmount != 6:
                playerAmount = 4
            if len(players[item["code"]]) >= playerAmount:
                for player in players[item["code"]]:
                    curQueue.pop(curQueue.index(player))
                gameID = str(time.time()) + "_" + str(random.randint(0,65535))
                existingGames[gameID] = players[item["code"]]
                with open("existingGames/" + gameID + ".json", "w") as file:
                    outObj = {"players": players[item["code"]]}
                    file.write(outObj)
                players[item["code"]] = []
        with open("queue.json", "w") as file:
            file.write(curQueue)
        with open("existingGames.json", "w") as file:
            file.write(existingGames)
        return "refreshed"
    """
    def newRoom(token, name):
        with open("existingGames.json", "r") as file:
            existingGames = json.load(file)
        if len(existingGames) < 26**4:
            code = ""
            for _ in range(4):
                code += chr(random.randint(65, 90))
            while code in existingGames.keys():
                code = ""
                for _ in range(4):
                    code += chr(random.randint(65, 90))
            return "SUCCESS! Free code: " + code
        else:
            return "FAILED! Codes are full."
            

    def joinRoom(token, name, code):
        if len(code) != 4:
            return "ERROR: Invalid Code!"
        for letter in code:
            if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                return "ERROR: Invalid Code!"
            
        with open("existingGames.json", "r") as file:
            existingGames = json.load(file)
        
        if code in existingGames.keys():
            if len(existingGames[code]) < 4:
                existingGames[code].append({"token": token, "name": name, "host": False})
                host = False
            else:
                return "ERROR: Room #" + code + " is full!"
        else:
            existingGames[code] = [{"token": token, "name": name, "host": True}]
            host = True
        
        with open("existingGames.json", "w") as file:
            json.dump(existingGames, file)
        
        if host:
            return "SUCCESS! Created room #" + code
        else:
            return "SUCCESS! Joined room #" + code
            
    def leaveRoom(token, name):
        existingGames, gameID, _ = main.locateGame(token, name)
        if gameID == "<none>":
            return "ERROR: Not in room!"
        for code, players in existingGames.items():
            for player in players:
                if player["name"] == name:
                    existingGames[code].pop(player)

        with open("existingGames.json", "w") as file:
            json.dump(existingGames, file)
        
        return "SUCCESS! Left room."
        


    def gameInfo(token, name):
        #Determine if the game is running or not.
        _, gameID, players = main.locateGame(token, name)
        if gameID == "<none>":
            return "ERROR: Not in room!"
        if os.path.exists("existingGames/" + gameID + ".json"):#RUNNING
            #Third, load in the game state file.
            with open("existingGames/" + gameID + ".json", "r") as file:
                gameState = json.load(file)

            for player in gameState["players"]:
                if player["name"] == name:
                    oldTime = player["time"]
                    gameState["players"][gameState["players"].index(player)]["time"] = time.time()
                else:
                    if player["time"] + IDLE < time.time(): #If any player is idle....
                        main.endGame(gameID, "IDLE")

            for player in gameState["players"]:
                gameState["players"][gameState["players"].index(player)]["cardAmount"] = len(player["deck"])
                if player["name"] != name:
                    gameState["players"][gameState["players"].index(player)]["deck"] = ["obfuscated"]

            #IF GAME REACHED 9 POINTS:
            if gameState["scores"]["1"] + gameState["scores"]["2"] == 9:
                main.endGame(gameID)

            #NOW CHECKING TRANSACTIONS
            translogs = "existingGames/" + gameID + " " + name + ".csv"
            if os.path.exists(translogs):
                with open(translogs, "r") as file:
                    transactions = file.read()
                os.remove(translogs)
            else:
                transactions = ""
            

            #Last, send the obfuscated gameState file. We need to add the transactions.
            return "PLAYING;" + json.dumps(gameState) + ";" + transactions
    
        else:#WAITING
            ret = players
            for i in range(len(ret)):
                ret[i]["token"] = "obfuscated"
            return "WAITING;" + gameID + ";" + json.dumps(ret)
    
    def startGame(token, name):
        _, gameID, players = main.locateGame(token, name)
        if gameID == "<none>":
            return "ERROR: Not in room!"
        for player in players:
            if player["token"] == token:
                if player["host"]:
                    if len(players) == 4:
                        #STARTING GAME
                        #1st: Shuffle cards.
                        cardList = lib.cards
                        random.shuffle(cardList)
                        gameState = {}
                        gameState["players"] = []
                        playerid = 1
                        for player in players:
                            #1 2 is team 1, 3 4 is team 2, 1 starts
                            cur = {"name": player["name"], "time": time.time()}
                            if playerid == 1:
                                cur["active"] = True
                            else:
                                cur["active"] = False
                            if playerid <= 2:
                                cur["team"] = 1
                            else:
                                cur["team"] = 2
                            if playerid % 2 == 0:
                                cur["cardAmount"] = 14
                                cur["deck"] = []
                                for _ in range(14):
                                    cur["deck"].append(cardList[-1])
                                    cardList.pop()
                            else:
                                cur["cardAmount"] = 13
                                cur["deck"] = []
                                for _ in range(13):
                                    cur["deck"].append(cardList[-1])
                                    cardList.pop()
                            
                            playerid += 1
                            gameState["players"].append(cur)

                            gameState["scores"] = {"1": 0, "2": 0}
                        
                        with open("existingGames/" + gameID + ".json", "w") as file:
                            json.dump(gameState, file)

                        return "SUCCESS! Game started."
                    else:
                        return "ERROR: Room not full!"
                else:
                    return "ERROR: You are not the host!"

    def askCard(token, name, target, card):
        gameState, gameID, _ = main.locateGame(token, name)
        if gameID == "<none>":
            return "ERROR: Not in room!"
        for player in gameState["players"]:
            if player["name"] == name:
                if player["active"]:
                        
                    #Check if player can ask for card
                    if card in player["deck"]:
                        return "ERROR: You already have this card!"
                    groupind, _ = lib.groupID(card)

                    if len(player["deck"]) == 0:
                        return "ERROR: You already died!"

                    flag = True
                    for handcard in player["deck"]:
                        loopgroupind, _ = lib.groupID(handcard)
                        if loopgroupind == groupind:
                            flag = False

                    if flag:
                        return "ERROR: You do not have a card in this group!"

                    flag = True
                    
                    for potTarget in gameState["players"]:
                        if potTarget["name"] == target:
                            if potTarget["team"] == player["team"]:
                                return "ERROR: Thats your teammate!"

                            flag = False
                            if card in potTarget["deck"]:
                                gameState["players"][gameState["players"].index(potTarget)]["deck"].remove(card)
                                gameState["players"][gameState["players"].index(player)]["deck"].append(card)
                                asked = True
                            else:
                                gameState["players"][gameState["players"].index(player)]["active"] = False
                                gameState["players"][gameState["players"].index(potTarget)]["active"] = True
                                asked = False

                    if flag:
                        return "ERROR: Player does not exist!"
                else:
                    return "ERROR: Not your turn!"
        
        with open("existingGames/" + gameID + ".json", "w") as file:
            json.dump(gameState, file)
        
        if asked:
            for player in gameState["players"]:
                with open('existingGames/' + gameID + " " + player["name"] + ".csv", "a") as file:
                    file.write(str(time.time()) + "," + name + "," + target + "," + card + ",obtained\n")
            return "SUCCESS! Obtained " + card
        else:
            for player in gameState["players"]:
                with open('existingGames/' + gameID + " " + player["name"] + ".csv", "a") as file:
                    file.write(str(time.time()) + "," + name + "," + target + "," + card + ",failed\n")
            return "SUCCESS! Failed to obtain " + card
    
    def declare(token, name, declaration):
        #declaration should contain all data for the declaration.
        #First digit: Group of card.
        #2-7th digit: Who has that certain card.
        gameState, gameID, _ = main.locateGame(token, name)
        if gameID == "<none>":
            return "ERROR: Not in room!"
        for letter in declaration:
            if letter not in "0123456789":
                return "ERROR: Invalid declaration!"

        for player in gameState["players"]:
            if player["name"] == name:
                team = player["team"]
        
        if len(declaration) == 1:
            cardCount = 0
            for player in gameState["players"]:
                if player["team"] == team:
                    for card in player["deck"]:
                        if card in lib.cardArray[int(declaration)]:
                            cardCount += 1
            if cardCount == 6:
                flag = True
        else:
            flag = True
            try:
                cardID = 0
                for card in lib.cardArray[int(declaration[0])]:
                    if card not in gameState["players"][int(declaration[cardID])]["deck"]:
                        flag = False
                    if gameState["players"][int(declaration[cardID])]["team"] != team:
                        flag = False
                    cardID += 1
            except IndexError:
                flag = False

        for player in gameState["players"]:
            for card in player["deck"]:
                if card in lib.cardArray[int(declaration[0])]:
                    gameState["players"]["deck"].pop(card)

        if flag: #If correct declaration:
            gameState["scores"][str(team)] += 1

            with open("existingGames/" + gameID + ".json", "w") as file:
                json.dump(gameState, file)
            for player in gameState["players"]:
                with open('existingGames/' + gameID + " " + player["name"] + ".csv", "a") as file:
                    file.write(str(time.time()) + "," + player + ",<none>," + declaration[0] + ",succeeded\n")
            
            return "SUCCESS! Declaration succeeded."
        else:
            gameState["scores"][str(3-team)] += 1

            with open("existingGames/" + gameID + ".json", "w") as file:
                json.dump(gameState, file)
            for player in gameState["players"]:
                with open('existingGames/' + gameID + " " + player["name"] + ".csv", "a") as file:
                    file.write(str(time.time()) + "," + player + ",<none>," + declaration[0] + ",failed\n")
            
            return "SUCCESS! Declaration failed."
    
    def endGame(gameID, reason = "FINISH"):
        with open("existingGames/" + gameID + ".json", "r") as file:
            gameState = json.load(file)
        
        if "ENDED" in gameState.keys():
            return
        
        gameState["ENDED"] = reason
        gameState["ENDTIME"] = time.time()

        with open("existingGames/" + gameID + ".json", "w") as file:
            json.dump(gameState, file)
    
    def selfRefresh():
        gameStateList = []
        for dir in os.listdir("existingGames"):
            if dir[-5:] == ".json":
                gameStateList.append(dir)
        for filename in gameStateList:
            with open("existingGames/"+filename, "r") as file:
                gameState = json.load(file)
            
            if "ENDED" in gameState.keys():
                if gameState["ENDTIME"] < time.time()-IDLE:
                    with open('existingTokens.csv', "r") as file:
                        allTokens = file.read().split("\n")

                    for line in allTokens:
                        for player in gameState['players']:
                            if line.split(",")[0] == player["name"]:
                                allTokens.remove(line)
                    with open('existingTokens.csv', "w") as file:
                        for line in allTokens:
                            file.write(line[0] + "," + line[1] + "," + line[2] + "\n")
                                
                    try:
                        # Loop through all files in the folder
                        for filename in os.listdir("existingGames/"):
                                # Get the full path of the file
                            file_path = os.path.join("existingGames/", filename)
                            # Check if it's a file and starts with the specified string
                            if os.path.isfile(file_path) and filename.startswith(filename[0:4]):
                                os.remove(file_path)
                                #print(f"Removed: {file_path}")
                    except Exception as e:
                        print(f"An error occurred (file deletion): {e}")

                    with open("existingGames.json", "r") as file:
                        allGames = json.load(file)
                    allGames[filename[:-5]] = None
                    with open("existingGames.json", "w") as file:
                        json.dump(allGames, file)
        return "Refreshed"