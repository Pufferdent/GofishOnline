from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget, QGridLayout, QMessageBox
)
from socketHelper import *
from lib import *
import json
import os
import csv
import sys

with open("texture/config.json", "r") as f:
    config = json.load(f)


class Ui_MainWindow(object):
    def __init__(self):
        self.token = "<none>"

        self.ReadFromFileButtonClicked()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(config["baseWindow"]["mainSize"][0], config["baseWindow"]["mainSize"][1])
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Game = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.Game.setGeometry(QtCore.QRect(config["baseWindow"]["gameSize"][0], config["baseWindow"]["gameSize"][1], config["baseWindow"]["gameSize"][2], config["baseWindow"]["gameSize"][3]))
        self.Game.setObjectName("Game")
        self.LoginPage = QtWidgets.QWidget()
        self.LoginPage.setObjectName("LoginPage")
        self.InputName = QtWidgets.QLineEdit(parent=self.LoginPage)
        self.InputName.setGeometry(QtCore.QRect(30, 40, 113, 20))
        self.InputName.setObjectName("InputName")
        self.InputPassword = QtWidgets.QLineEdit(parent=self.LoginPage)
        self.InputPassword.setGeometry(QtCore.QRect(30, 80, 113, 20))
        self.InputPassword.setObjectName("InputPassword")
        self.LoginResponse = QtWidgets.QLabel(parent=self.LoginPage)
        self.LoginResponse.setGeometry(QtCore.QRect(250, 70, 141, 21))
        self.LoginResponse.setObjectName("LoginResponse")
        self.Login = QtWidgets.QPushButton(parent=self.LoginPage)
        self.Login.setGeometry(QtCore.QRect(350, 160, 75, 24))
        self.Login.setObjectName("Login")
        self.Login.clicked.connect(self.LoginButtonClicked)
        self.ReadFromFile = QtWidgets.QPushButton(parent=self.LoginPage)
        self.ReadFromFile.setGeometry(QtCore.QRect(180, 160, 161, 24))
        self.ReadFromFile.setObjectName("ReadFromFile")
        self.ReadFromFile.clicked.connect(self.ReadFromFileButtonClicked)
        self.Register = QtWidgets.QPushButton(parent=self.LoginPage)
        self.Register.setGeometry(QtCore.QRect(90, 160, 75, 24))
        self.Register.setObjectName("Register")
        self.Register.clicked.connect(self.RegisterButtonClicked)




        self.Game.addTab(self.LoginPage, "")
        self.GamePage = QtWidgets.QWidget()
        self.GamePage.setObjectName("GamePage")

        self.mainGame = gameWidget(parent=self.GamePage)

        self.mainGame.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.mainGame.setObjectName("mainGame")
        self.Game.addTab(self.GamePage, "")




        self.Statistics = QtWidgets.QWidget()
        self.Statistics.setObjectName("Statistics")
        self.Game.addTab(self.Statistics, "")
        MainWindow.setCentralWidget(self.centralwidget)





        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        self.menuGame = QtWidgets.QMenu(parent=self.menubar)
        self.menuGame.setObjectName("menuGame")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuGame.menuAction())



        self.retranslateUi(MainWindow)
        self.Game.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", config["baseWindow"]["mainTitle"]))
        self.InputName.setText(_translate("MainWindow", self.account["name"]))
        self.InputPassword.setText(_translate("MainWindow", self.account["password"]))
        self.LoginResponse.setText(_translate("MainWindow", "Please Login."))
        self.Login.setText(_translate("MainWindow", "Login"))
        self.ReadFromFile.setText(_translate("MainWindow", "Read From File"))
        self.Register.setText(_translate("MainWindow", "Register"))
        self.Game.setTabText(self.Game.indexOf(self.LoginPage), _translate("MainWindow", "Account"))
        self.Game.setTabText(self.Game.indexOf(self.GamePage), _translate("MainWindow", "Game"))
        self.Game.setTabText(self.Game.indexOf(self.Statistics), _translate("MainWindow", "Statistics"))
        self.menu.setTitle(_translate("MainWindow", "Login"))
        self.menuGame.setTitle(_translate("MainWindow", "Game"))
    
    def LoginButtonClicked(self):
        string = getRequest(f"/LOGIN {self.InputName.text()} {self.InputPassword.text()}")
        if "ERROR" in string:
            self.LoginResponse.setText(string)
        else:
            self.LoginResponse.setText("Login Successful")
            self.account["name"] = self.InputName.text()
            self.account["password"] = self.InputPassword.text()
            self.mainGame.setAccount(self.account)
            with open("account.json", "w") as file:
                json.dump(self.account, file)
            self.token = string
            self.mainGame.token = string
    
    def ReadFromFileButtonClicked(self):
        if not os.path.exists('account.json'):
            with open('account.json', "w") as file:
                pass
            self.account = {"name": "Input Name", "password": "Input Password"}
        else:
            #Load login data
            with open('account.json', 'r') as file:
                self.account = json.load(file)

    def RegisterButtonClicked(self):
        string = getRequest(f"/NEWACC {self.InputName.text()} {self.InputPassword.text()}")
        if "ERROR" in string:
            self.LoginResponse.setText(string)
        else:
            self.LoginResponse.setText("Register Successful")
            self.token = string
            self.LoginButtonClicked()
        

class gameStateHelper():
    def __init__(self, state):
        self.state = state

    def getPlayers(self):
        return self.state["players"]


class gameWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(1920, 1080)  # Set fixed size for the game window
        self.setStyleSheet("background-color: black;")  # Background color of the game
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.declareButton = QtWidgets.QPushButton(parent=self)
        self.declareButton.setGeometry(QtCore.QRect(700, 500, 100, 40))  # Adjust position and size
        self.declareButton.setText("Declare")
        self.declareButton.clicked.connect(self.on_declare_clicked)

        self.background = QPixmap("texture/background.png")
        self.frame = 0
        self.infoMsg = "INFO"
        self.displayMsg = ""
        self.token = "EMPTY"
        self.game = "EMPTY"
        self.text_input = None

        # Set up a timer to update the game state
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)  # Approximately 60 frames per second

    def setAccount(self, account):
        self.account = account

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 16))
        painter.setPen(QColor("black"))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        #Render Background
        painter.drawPixmap(0, 0, self.background)

        #Render InfoMsg
        painter.drawText(10, 20, self.displayMsg)

        """if self.text_input is not None:
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(self.text_input.pos(), self.text_input.text())
            painter.setPen(QColor("black"))"""

        if self.game == "PLAYING":
            if not hasattr(self, "playerArrange"):
                self.playerArrange = {}
                players = [
                    {"x": 0, "y": 0, "count": 0},  # Player 1
                    {"x": 0, "y": 0, "count": 0},  # Player 2
                    {"x": 0, "y": 0, "count": 0}  # Player 3
                ]
                team = -1
                i = 0
                for player in self.gameState["players"]:
                    if player["name"] == self.account["name"]:
                        unsorteddeck = player["deck"]
                        team = player["team"]
                        self.playerArrange["Self"] = self.gameState["players"].index(player)
                        deck = []
                        for set in cards:
                            for card in set:
                                if card in unsorteddeck:
                                    deck.append(card)

                    else:
                        players[i]["count"] = player["cardAmount"]
                        players[i]["name"] = player["name"]
                        i += 1

                i = 0
                for player in self.gameState["players"]:
                    if player["name"] != self.account["name"] and player["team"] == team:
                        players[i]["x"] = config["game"]["players"][1][0]
                        players[i]["y"] = config["game"]["players"][1][1]
                        self.playerArrange["Side"] = self.gameState["players"].index(player)
                    if player["name"] != self.account["name"]:
                        i += 1
                print(self.playerArrange)
            else:
                players = [
                    {"x": 0, "y": 0, "count": 0},  # Player 1
                    {"x": 0, "y": 0, "count": 0},  # Player 2
                    {"x": 0, "y": 0, "count": 0}  # Player 3
                ]
                i = 0
                for player in self.gameState["players"]:
                    if player["name"] != self.account["name"]:
                        players[i]["count"] = player["cardAmount"]
            
            
            # Render deck (your cards)
            card_x = config["game"]["players"][0][0]  # Initial x position for card rendering
            card_y = config["game"]["players"][0][1]  # Adjust y to render at the bottom
            card_spacing = min(30, config["game"]["cardLength"]//len(deck))  # Spacing between cards
            painter.drawText(card_x, card_y, str(len(deck)))
            for card in deck:
                card_image_path = f"texture/cards/{card}.png"
                if os.path.exists(card_image_path):
                    card_pixmap = QPixmap(card_image_path)
                    painter.drawPixmap(card_x, card_y, card_pixmap.scaled(config["game"]["cardSize"][0], config["game"]["cardSize"][1]))  # Scale cards to fit
                card_x += card_spacing  # Adjust x position for next card


            #Generate coords for opponents
            first = True
            for i in range(3):
                if players[i]["x"] == 0:
                    if first:
                        players[i]["x"] = config["game"]["players"][2][0]
                        players[i]["y"] = config["game"]["players"][2][1]
                        first = False
                    else:
                        players[i]["x"] = config["game"]["players"][3][0]
                        players[i]["y"] = config["game"]["players"][3][1]

            
            # Render other players' cards as card backs
            back_image_path = os.path.join("texture/cards", "Back.png")
            if os.path.exists(back_image_path):
                back_pixmap = QPixmap(back_image_path)
                
                for player in players:
                    card_x = player["x"]
                    card_y = player["y"]
                    for i in range(player["count"]):
                        painter.drawPixmap(card_x, card_y, back_pixmap.scaled(config["game"]["backSize"][0], config["game"]["backSize"][1]))
                        card_x += min(15, config["game"]["backLength"]//player["count"])  # Overlap to indicate multiple cards
                    painter.drawText(player["x"], player["y"], str(player["name"]) + ": " + str(player["count"]))
            

            #if self.gameState["active"] == True:
            #    if self.gameState["turn"] == self.account["name"]:
            #        painter.drawText(30, 30, "Your turn")
            #    else:
            #        painter.drawText(30, 30, "Waiting for " + self.gameState["turn"])




    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_T:
            if self.text_input is None:
                self.create_text_input(30, 550)
            else:
                self.text_input.setFocus()


    def create_text_input(self, x, y):
        """Create a text input widget (QLineEdit) at the clicked position."""
        # Create a QLineEdit widget for text input
        self.text_input = QtWidgets.QLineEdit(self)
        self.text_input.move(x, y)  # Move to the clicked position
        self.text_input.setFocus()  # Focus the text input for immediate typing
        self.text_input.show()  # Show the text input widget

        # Make the QLineEdit widget transparent so it doesn't obstruct game visuals
        self.text_input.setStyleSheet("background-color: transparent; color: white;")

        # Connect signal for when the user finishes typing (e.g., pressing Enter)
        self.text_input.returnPressed.connect(self.on_text_input)
    
    def on_text_input(self):
        """Handle the text input when user presses Enter."""
        text = self.text_input.text()

        if text.lower()[0:5] == "/join":
            getRequest(f"/MAINGAME {self.token} JOIN " + text.upper()[6:])
        
        if text.lower()[0:6] == "/start":
            getRequest(f"/MAINGAME {self.token} START")
        
        if text.lower()[0:6] == "/leave":
            getRequest(f"/MAINGAME {self.token} LEAVEROOM")

        self.text_input.hide()
        self.setFocus()
        self.text_input = None

    def inPlayerRange(self, x, y):
        if x > config["game"]["players"][2][0] and x < config["game"]["players"][2][0] + config["game"]["backLength"] and y > config["game"]["players"][2][1] and y < config["game"]["players"][2][1] + config["game"]["backSize"][1]:
            return "Left"
        if x > config["game"]["players"][3][0] and x < config["game"]["players"][3][0] + config["game"]["backLength"] and y > config["game"]["players"][3][1] and y < config["game"]["players"][3][1] + config["game"]["backSize"][1]:
            return "Right"
        if x > config["game"]["players"][1][0] and x < config["game"]["players"][1][0] + config["game"]["backLength"] and y > config["game"]["players"][1][1] and y < config["game"]["players"][1][1] + config["game"]["backSize"][1]:
            return "Side"
        if x > config["game"]["players"][0][0] and x < config["game"]["players"][0][0] + config["game"]["cardLength"] and y > config["game"]["players"][0][1] and y < config["game"]["players"][0][1] + config["game"]["cardSize"][1]:
            return "Self"
        return "None"
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            #Ask card trigger:
            trigger = self.inPlayerRange(pos.x(), pos.y())
            if trigger != "None" and trigger != "Self":
                self.askTarget = trigger
                self.cardSelect = CardSelector()
                self.cardSelect.show()
    
    def update_game(self):

        self.frame += 1

        if self.frame%60 == 0 and self.token != "EMPTY":
            self.infoMsg = getRequest(f"/MAINGAME {self.token} INFO")

        if "ERROR" in self.infoMsg or "FAILED" in self.infoMsg:
            self.displayMsg = self.infoMsg
        else:
            key = self.infoMsg.split(";")
            if key[0] == "WAITING":
                players = json.loads(key[2])
                self.game = "WAITING"
                self.displayMsg = "Waiting in " + key[1] + ": " +str([player["name"] for player in players])
            elif key[0] == "PLAYING":
                self.gameState = json.loads(key[1])
                self.transactions = csv.reader(key[2].split("\n"))
                self.game = "PLAYING"
                self.displayMsg = ""

        if hasattr(self, "cardSelect") and self.cardSelect != None:
            self.selectedCard = self.cardSelect.selectedCard
            if hasattr(self, "selectedCard") and self.selectedCard != None:
                self.cardSelect.close()
                self.cardSelect = None
        
        if hasattr(self, "selectedCard") and self.selectedCard != None:
            response = getRequest(f"/MAINGAME {self.token} ASK {self.gameState['players'][self.playerArrange[self.askTarget]]['name']} {self.selectedCard}")
            self.displayMsg = response
            self.selectedCard = None

        if hasattr(self, "groupSelect") and self.groupSelect != None:
            self.selectedGroup = self.groupSelect.selectedGroup
            if hasattr(self, "selecetedGroup") and self.selectedGroup != None:
                self.groupSelect.close()
                self.groupSelect = None
        
        if hasattr(self, "selectedGroup") and self.selectedGroup != None:
            response = getRequest(f"/MAINGAME {self.token} DECLARE {self.selectedGroup}")
            displayMsg = response
            self.selectedCard = None
        # Trigger a repaint to update the display
        self.update()
    
    def on_declare_clicked(self):
        self.groupSelect = GroupSelector()
        self.groupSelect.show()



class GroupSelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Group Selection")
        self.resize(300, 200)

        self.groups = cards
        self.setFocus()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Label to display instructions
        self.instruction_label = QLabel("Select a group:")
        layout.addWidget(self.instruction_label)

        # Stacked widget for group and card selection
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Group selection page
        self.group_page = QWidget()
        self.group_layout = QGridLayout()

        for i in range(9):
            group_label = QLabel()
            group_label.setPixmap(QPixmap(f"texture/groups/{i}.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
            group_label.mousePressEvent = lambda event, g=i: self.ret(g)
            self.group_layout.addWidget(group_label, i // 3, i % 3)

        self.group_page.setLayout(self.group_layout)
        self.stacked_widget.addWidget(self.group_page)

        # Card selection page
        self.card_page = QWidget()
        self.card_layout = QGridLayout()
        self.card_page.setLayout(self.card_layout)
        self.stacked_widget.addWidget(self.card_page)

        self.setLayout(layout)

    def ret(self, group):
        self.selectedGroup = group
        self.hide()

    def focusOutEvent(self, event):
        # Hide the widget when it loses focus
        self.hide()
        super().focusOutEvent(event)

class CardSelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Card Selection")
        self.resize(300, 200)

        self.groups = cards
        self.setFocus()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Label to display instructions
        self.instruction_label = QLabel("Select a group to begin:")
        layout.addWidget(self.instruction_label)

        # Stacked widget for group and card selection
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Group selection page
        self.group_page = QWidget()
        self.group_layout = QGridLayout()

        for i in range(9):
            group_label = QLabel()
            group_label.setPixmap(QPixmap(f"texture/groups/{i}.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
            group_label.mousePressEvent = lambda event, g=i: self.show_cards_in_group(g)
            self.group_layout.addWidget(group_label, i // 3, i % 3)

        self.group_page.setLayout(self.group_layout)
        self.stacked_widget.addWidget(self.group_page)

        # Card selection page
        self.card_page = QWidget()
        self.card_layout = QGridLayout()
        self.card_page.setLayout(self.card_layout)
        self.stacked_widget.addWidget(self.card_page)

        self.setLayout(layout)

    def show_cards_in_group(self, group_index):
        # Clear previous card labels
        for i in reversed(range(self.card_layout.count())):
            widget = self.card_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add card images for the selected group
        for i, card in enumerate(self.groups[group_index]):
            card_path = os.path.join("texture/cards", f"{card}.png")
            card_label = QLabel()

            if os.path.exists(card_path):
                pixmap = QPixmap(card_path).scaled(50, 70, Qt.AspectRatioMode.KeepAspectRatio)
                card_label.setPixmap(pixmap)
            else:
                card_label.setText("Missing Image")
                card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_label.mousePressEvent = lambda event, c=card: self.select_card(c)
            self.card_layout.addWidget(card_label, i // 3, i % 3)

        # Update instruction label and switch page
        self.instruction_label.setText(f"Select a card from Group {group_index + 1}:")
        self.stacked_widget.setCurrentWidget(self.card_page)

    def select_card(self, card):
        self.selectedCard = card
        self.hide()

    def focusOutEvent(self, event):
        # Hide the widget when it loses focus
        self.hide()
        super().focusOutEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())