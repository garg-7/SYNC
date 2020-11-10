import sys, socket, time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton, QRadioButton, QMainWindow, QButtonGroup, QLineEdit
from PyQt5.QtWidgets import QWidget, QComboBox, QStackedWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QStackedLayout

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from _thread import start_new_thread
from threading import Thread
import pygame

pygame.mixer.init()
pygame.mixer.music.load('stay.mp3')

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

def startServerWindow(window):
    sWindow = QWidget()
    sWindow.setWindowTitle('Sync')
    print("[INFO] Server operation chosen.")
    intro = QLabel("Operating as a server")
    intro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
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
    refBtn = QPushButton("Refresh")
    refBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
    refBtn.clicked.connect(lambda: updateClients())
    sLayout = QGridLayout()
    sLayout.addWidget(intro, 0,0,1,3)
    sLayout.addWidget(hostKey, 1,0)
    sLayout.addWidget(hostVal, 1,1)
    sLayout.addWidget(portKey, 2,0)
    sLayout.addWidget(portVal, 2,1)
    sLayout.addWidget(msg, 3,0,1,3)
    sLayout.addWidget(refBtn, 4,1)
    sWindow.setLayout(sLayout)
    sWindow.show()
    window.close()
    start_new_thread(startListening, (host, port))

def startClientWindow(window):
    cWindow = QWidget()
    cWindow.setWindowTitle('Sync')
    print("[INFO] Client operation chosen.")
    intro = QLabel("Operating as a client")
    intro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
    hostWidget = QLineEdit()
    hostWidget.setPlaceholderText("Say Dell-G3")
    portWidget = QLineEdit()
    portWidget.setPlaceholderText("Say 9077")
    hostKey = QLabel("Enter Host: ")
    hostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
    portKey = QLabel("Enter Port: ")
    portKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
    cntBtn = QPushButton("Connect")
    cntBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
    cntBtn.clicked.connect(lambda: attemptConnection())
    cLayout = QGridLayout()
    cLayout.addWidget(intro, 0,0,1,3)
    cLayout.addWidget(hostKey, 1,0)
    cLayout.addWidget(hostWidget, 1,1)
    cLayout.addWidget(portKey, 2,0)
    cLayout.addWidget(portWidget, 2,1)
    # layout.addWidget(msg, 3,0,1,3)
    cLayout.addWidget(cntBtn, 3,1)
    cWindow.setLayout(cLayout)
    cWindow.show()
    window.close()
    window.deleteLater()

def decide(window, id):
    if id==1:
        # create a new layout and set that into the window
        startServerWindow(window)
    else:
        # create the client layout
        startClientWindow(window)

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


# proBtn = QPushButton("Proceed")
# proBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

def startMainWindow():
    mainWindow = QWidget()
    mainwindow.setWindowTitle('Sync')
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
    bGroup.addButton(serverBtn, 1)
    bGroup.addButton(clientBtn, 2)
    layout = QGridLayout()
    layout.addWidget(intro, 0,0,1,3)
    layout.addWidget(serverBtn, 1,0, Qt.AlignCenter)
    layout.addWidget(clientBtn, 1,2, Qt.AlignCenter)
    layout.addWidget(nextBtn, 3,1)

    stackedWidget = QStackedWidget()
    mainIdx = stackedWidget.addWidget(mainWindow)
    sIdx = stackedWidget.addWidget(sWindow)
    cIdx = stackedWidget.addWidget(cWindow)

    nextBtn.clicked.connect(lambda: decide(window, bGroup.checkedId()))


    mainLayout = QVBoxLayout()
    mainLayout.addLayout(stackedWidget)
    window.setLayout(mainLayout)
    
    pages = QComboBox()
    pages.addItem()
    window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startMainWindow()
    sys.exit(app.exec_())