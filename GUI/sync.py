import sys, socket, time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton, QRadioButton, QMainWindow, QButtonGroup, QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from _thread import start_new_thread
from threading import Thread
import pygame

pygame.mixer.init()
pygame.mixer.music.load('stay.mp3')

app = QApplication(sys.argv)
window = QWidget()
hostWidget = QLineEdit()
hostWidget.setPlaceholderText("Say Dell-G3")
portWidget = QLineEdit()
portWidget.setPlaceholderText("Say 9077")

hostKey = QLabel("Enter Host: ")
hostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
portKey = QLabel("Enter Port: ")
portKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

clients = []
updatedClients = []

def startListening(host, port):
    s = socket.socket()
    s.bind((host,port))
    s.listen()
    ID = 0
    while ID<2:
        clientsocket, address = s.accept()
        clients.append((clientsocket, address))
        ID+=1
        clientsocket.send('Welcome!'.encode())
    return

def mode(id):
    global hostKey, hostWidget, portKey, portWidget
    if id==1:
        # create a new layout and set that into the window
        print("[INFO] Server operation chosen.")
        intro.setText("Operating as a server")
        layout.removeWidget(serverBtn)
        serverBtn.deleteLater()
        layout.removeWidget(clientBtn)
        clientBtn.deleteLater()
        layout.removeWidget(nextBtn)
        nextBtn.deleteLater()
        host = socket.gethostname()
        port = 9077
        hostKey = QLabel("Host: ")
        hostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        hostVal = QLabel(host)
        hostVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        portKey = QLabel("Port: ")
        portKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        portVal = QLabel(str(port))
        portVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        msg = QLabel("Share this info with your clients!")
        msg.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        layout.addWidget(hostKey, 1,0)
        layout.addWidget(hostVal, 1,1)
        layout.addWidget(portKey, 2,0)
        layout.addWidget(portVal, 2,1)
        layout.addWidget(msg, 3,0,1,3)
        layout.addWidget(refBtn, 4,1)
        start_new_thread(startListening, (host, port))
    else:
        # create the client layout
        print("[INFO] Client operation chosen.")
        intro.setText("Operating as a client")
        layout.removeWidget(serverBtn)
        serverBtn.deleteLater()
        layout.removeWidget(clientBtn)
        clientBtn.deleteLater()
        layout.removeWidget(nextBtn)
        nextBtn.deleteLater()
        layout.addWidget(hostKey, 1,0)
        layout.addWidget(hostWidget, 1,1)
        layout.addWidget(portKey, 2,0)
        layout.addWidget(portWidget, 2,1)
        # layout.addWidget(msg, 3,0,1,3)
        layout.addWidget(cntBtn, 3,1)

def getLayout(serverBtn, clientBtn, nextBtn):
    layout = QGridLayout()
    layout.addWidget(intro, 0,0,1,3)
    layout.addWidget(serverBtn, 1,0, Qt.AlignCenter)
    layout.addWidget(clientBtn, 1,2, Qt.AlignCenter)
    layout.addWidget(nextBtn, 3,1)
    return layout

def updateClients():
    if len(clients)!=0:
        ID = len(updatedClients)
        for c in clients:
            if c not in updatedClients:
                ID = len(updatedClients)
                layout.addWidget(QLabel(f"Connected with {c[1]}, allotted ID={ID+1}"), 4+(ID+1),0,1,3)
                if ID==0:
                    layout.addWidget(proBtn, 4+len(updatedClients)+1,4)
                updatedClients.append(c)
    return

def attemptConnection():
    host = hostWidget.text()
    port = int(portWidget.text())
    s = socket.socket()
    s.connect((host, port))
    layout.removeWidget(hostKey)
    layout.removeWidget(hostWidget)
    layout.removeWidget(portKey)
    layout.removeWidget(portWidget)
    hostKey.deleteLater()
    hostWidget.deleteLater()
    portKey.deleteLater()
    portWidget.deleteLater()
    connected = QLabel("Connected!")
    connected.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
    layout.addWidget(connected, 1,0,1,3)
    s.recv(1024)
    layout.removeWidget(cntBtn)
    cntBtn.deleteLater()


window.setWindowTitle('Sync')
intro = QLabel("What do you want to be?")
intro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")


serverBtn = QRadioButton("Server")
serverBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
icon = QIcon('images/server.png')
serverBtn.setIcon(icon)
serverBtn.setIconSize(QSize(75,75)) 

bGroup = QButtonGroup()

clientBtn = QRadioButton("Client")
clientBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
icon = QIcon('images/client.png')
clientBtn.setIcon(icon)
clientBtn.setIconSize(QSize(75,75))

serverBtn.setChecked(True)
nextBtn = QPushButton("Next")
nextBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

 
refBtn = QPushButton("Refresh")
nextBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

proBtn = QPushButton("Proceed")
proBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

cntBtn = QPushButton("Connect")
cntBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")


bGroup.addButton(serverBtn, 1)
bGroup.addButton(clientBtn, 2)

layout = getLayout(bGroup.button(1), bGroup.button(2), nextBtn)

nextBtn.clicked.connect(lambda: mode(bGroup.checkedId()))
refBtn.clicked.connect(lambda: updateClients())
cntBtn.clicked.connect(lambda: attemptConnection())
window.setLayout(layout)
window.show()
sys.exit(app.exec_())