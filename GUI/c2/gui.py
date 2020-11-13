from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QLabel, QRadioButton, QPushButton, QLineEdit, QButtonGroup, QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os

MUSIC_PATH = 'music'
class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main, host, port, maxClients):
        Main.setObjectName("Main")
        self.sHost = host               # host name of server
        self.sPort = port               # port at which server accepts connections
        self.maxClients = maxClients    # max number of clients to connect with the server
        self.QtStack = QtWidgets.QStackedLayout()

        self.stack1 = QtWidgets.QWidget()   # the main screen
        self.stack2 = QtWidgets.QWidget()   # server intro
        self.stack3 = QtWidgets.QWidget()   # client enter info
        self.stack4 = QtWidgets.QWidget()   # client connected
        self.stack5 = QtWidgets.QWidget()   # server w/ client list and verify
        self.stack6 = QtWidgets.QWidget()   # server player

        # initialize UI windows
        self.startUI()
        self.serverUI(host, port)
        self.clientUI()
        self.clientConnectedUI()
        self.clientsFileVerify()
        self.clientsListUI()

        # add UI windows to Qt Stack
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)

    def startUI(self):
        self.stack1.setFixedSize(500,200)
        self.stack1.setWindowTitle("Sync")
        
        # Intro msg
        self.intro = QLabel("What do you want to be?")
        self.intro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Server Button
        self.serverBtn = QRadioButton("Server")
        self.serverBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
        icon = QIcon('images/server.png')
        self.serverBtn.setIcon(icon)
        self.serverBtn.setIconSize(QSize(75,75))
        self.serverBtn.setChecked(True)

        # Client Button
        self.clientBtn = QRadioButton("Client")
        self.clientBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
        icon = QIcon('images/client.png')
        self.clientBtn.setIcon(icon)
        self.clientBtn.setIconSize(QSize(75,75))

        # Button group to maintain exclusivity
        self.bGroup = QButtonGroup()
        self.bGroup.addButton(self.serverBtn, 1)
        self.bGroup.addButton(self.clientBtn, 2)

        # Next Button
        self.nextBtn = QPushButton("Next")
        self.nextBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
        
        # Integrate grid layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.intro, 0,0,1,3)
        self.layout.addWidget(self.serverBtn, 1,0, Qt.AlignCenter)
        self.layout.addWidget(self.clientBtn, 1,2, Qt.AlignCenter)
        self.layout.addWidget(self.nextBtn, 3,1)
        self.stack1.setLayout(self.layout)


    def serverUI(self, host, port):
        self.stack2.setFixedSize(500,200)
        self.stack2.setWindowTitle("Sync")
        
        # Server intro message
        self.sIntro = QtWidgets.QLabel("Operating as a server")
        self.sIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Server host key & val
        self.sHostKey = QLabel("Host: ")
        self.sHostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.sHostVal = QLabel(host)
        self.sHostVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        
        # Server port key & val
        self.sPortKey = QLabel("Port: ")
        self.sPortKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.sPortVal = QLabel(str(port))
        self.sPortVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        
        # Server msg
        self.sMsg = QLabel("Share this info with your clients!")
        self.sMsg.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # Server proceed button
        self.proBtn = QPushButton("Proceed")
        self.proBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # Integrate grid layout
        self.sLayout = QGridLayout()
        self.sLayout.addWidget(self.sIntro, 0,0,1,3)
        self.sLayout.addWidget(self.sHostKey, 1,0)
        self.sLayout.addWidget(self.sHostVal, 1,1)
        self.sLayout.addWidget(self.sPortKey, 2,0)
        self.sLayout.addWidget(self.sPortVal, 2,1)
        self.sLayout.addWidget(self.sMsg, 3,0,1,3)
        self.sLayout.addWidget(self.proBtn, 4, 1)
        self.stack2.setLayout(self.sLayout)

    def clientUI(self):
        self.stack3.setFixedSize(500,200)
        self.stack3.setWindowTitle("Sync")
        
        # client intro message
        self.cIntro = QLabel("Operating as a client")
        self.cIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Client host key & val
        self.cHostKey = QLabel("Host: ")
        self.cHostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.cHostVal = QLineEdit()
        self.cHostVal.setPlaceholderText("Say Dell-G3")
        
        # Client port key & val
        self.cPortKey = QLabel("Port: ")
        self.cPortKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.cPortVal = QLineEdit()
        self.cPortVal.setPlaceholderText("Say 9077")
        
        # client connect button
        self.cntBtn = QPushButton("Connect")
        self.cntBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # Integrate grid layout
        self.cLayout = QGridLayout()
        self.cLayout.addWidget(self.cIntro, 0,0,1,3)
        self.cLayout.addWidget(self.cHostKey, 1,0)
        self.cLayout.addWidget(self.cHostVal, 1,1,1,2)
        self.cLayout.addWidget(self.cPortKey, 2,0)
        self.cLayout.addWidget(self.cPortVal, 2,1,1,2)
        self.cLayout.addWidget(self.cntBtn, 4,1)
        self.stack3.setLayout(self.cLayout)
    
    def clientConnectedUI(self):
        self.stack4.setFixedSize(500,200)
        self.stack4.setWindowTitle("Sync")

        # client intro message
        self.cCIntro =  QtWidgets.QLabel("Operating as a client")
        self.cCIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Client welcome msg
        self.cConnected = QLabel("Connected!")
        self.cConnected.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # Integrate grid layout
        self.cCLayout = QGridLayout()
        self.cCLayout.addWidget(self.cCIntro, 0,0,1,3)
        self.cCLayout.addWidget(self.cConnected, 1,0,1,3)
        self.stack4.setLayout(self.cCLayout)

    def clientsFileVerify(self):
        self.stack5.setFixedWidth(500)
        self.stack5.setWindowTitle("Sync")
        
        # Server intro message
        self.cFVIntro = QtWidgets.QLabel("Operating as a server")
        self.cFVIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Server host key & val
        self.cFVHostKey = QLabel("Host: ")
        self.cFVHostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.cFVHostVal = QLabel(self.sHost)
        self.cFVHostVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        
        # Server port key & val
        self.cFVPortKey = QLabel("Port: ")
        self.cFVPortKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.cFVPortVal = QLabel(str(self.sPort))
        self.cFVPortVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        
        # clients list display
        self.cFVMsg = QLabel("Clients Connected:")
        self.cFVMsg.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # music pick drop down
        self.cFVmusicBox = QComboBox()
        
        for m in self.musicFiles:
            self.cFVmusicBox.addItem(m)
        
        # music helper label
        self.cFVmHelper = QLabel("Select Music")
        self.cFVmHelper.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # verify button
        self.vfyBtn = QPushButton("Verify")
        self.vfyBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # List of clients connected
        self.clientLabels = []
        for _ in range(self.maxClients):
            self.clientLabels.append(QLabel(""))

        # integrate into grid layout
        self.cFVLayout = QGridLayout()
        self.cFVLayout.addWidget(self.cFVIntro, 0,0,1,3)
        self.cFVLayout.addWidget(self.cFVHostKey, 1,0)
        self.cFVLayout.addWidget(self.cFVHostVal, 1,1)
        self.cFVLayout.addWidget(self.cFVPortKey, 2,0)
        self.cFVLayout.addWidget(self.cFVPortVal, 2,1)
        self.cFVLayout.addWidget(self.cFVMsg, 3,0,1,3)
        for i,c in enumerate(self.clientLabels):
            self.cFVLayout.addWidget(c, 3+(i+1),0,1,3)
        self.cFVLayout.addWidget(self.cFVmHelper, self.maxClients+4, 0)
        self.cFVLayout.addWidget(self.cFVmusicBox, self.maxClients+4, 1, 1, 2)
        self.cFVLayout.addWidget(self.vfyBtn, self.maxClients+5,1)

        self.stack5.setLayout(self.cFVLayout)

    def clientsListUI(self):
        self.stack6.setFixedWidth(500)
        self.stack6.setWindowTitle("Sync")
        
        # Server intro message
        self.cLIntro = QtWidgets.QLabel("Operating as a server")
        self.cLIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Server host key & val
        self.cLHostKey = QLabel("Host: ")
        self.cLHostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.cLHostVal = QLabel(self.sHost)
        self.cLHostVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        
        # Server port key & val
        self.cLPortKey = QLabel("Port: ")
        self.cLPortKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.cLPortVal = QLabel(str(self.sPort))
        self.cLPortVal.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # song name label
        self.songName = QLabel("")
        self.songName.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # file verifier label
        self.vfyMsg = QLabel("File verification complete: ")
        self.vfyMsg.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        
        self.filePresence = []
        # file verificatin results
        for _ in range(self.maxClients):
            self.filePresence.append(QLabel(""))
        
        # play button
        self.playBtn = QPushButton("Play")
        self.playBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # pause button
        self.pauseBtn = QPushButton("Pause")
        self.pauseBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # stop button
        self.stopBtn = QPushButton("Stop")
        self.stopBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
        
        # end button
        self.endBtn = QPushButton("End")
        self.endBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # back button
        self.backBtn = QPushButton("Go Back")
        self.backBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # integrate into grid layout
        self.cLLayout = QGridLayout()
        self.cLLayout.addWidget(self.cLIntro, 0,0,1,3)
        self.cLLayout.addWidget(self.cLHostKey, 1,0)
        self.cLLayout.addWidget(self.cLHostVal, 1,1)
        self.cLLayout.addWidget(self.cLPortKey, 2,0)
        self.cLLayout.addWidget(self.cLPortVal, 2,1)
        self.cLLayout.addWidget(self.songName, 3,1)
        self.cLLayout.addWidget(self.vfyMsg, 4, 0, 1, 3)
        for i,c in enumerate(self.filePresence):
            self.cLLayout.addWidget(c, 4+(i+1),0,1,3)
        self.cLLayout.addWidget(self.playBtn, self.maxClients+5,0)
        self.cLLayout.addWidget(self.pauseBtn, self.maxClients+5,1)
        self.cLLayout.addWidget(self.stopBtn, self.maxClients+5,2)
        self.cLLayout.addWidget(self.backBtn, self.maxClients+6, 1)
        self.cLLayout.addWidget(self.endBtn, self.maxClients+7, 0, 1, 3)
        self.stack6.setLayout(self.cLLayout)