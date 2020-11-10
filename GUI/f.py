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
        self.sHost = host
        self.sPort = port
        self.maxClients = maxClients
        self.QtStack = QtWidgets.QStackedLayout()

        self.stack1 = QtWidgets.QWidget()   # the main screen
        self.stack2 = QtWidgets.QWidget()   # server intro
        self.stack3 = QtWidgets.QWidget()   # client enter info
        self.stack4 = QtWidgets.QWidget()   # client connected
        self.stack5 = QtWidgets.QWidget()   # clients list

        self.stack1.setWindowTitle("Sync")
        self.stack2.setWindowTitle("Sync")
        self.stack3.setWindowTitle("Sync")
        self.stack4.setWindowTitle("Sync")
        self.stack5.setWindowTitle("Sync")

        self.startUI()
        self.serverUI(host, port)
        self.clientUI()
        self.clientConnectedUI()
        self.clientsListUI()

        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)

    def startUI(self):
        self.stack1.setFixedSize(500,200)
        #Intro msg
        self.intro = QLabel("What do you want to be?")
        self.intro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        #Server Button
        self.serverBtn = QRadioButton("Server")
        self.serverBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
        icon = QIcon('images/server.png')
        self.serverBtn.setIcon(icon)
        self.serverBtn.setIconSize(QSize(75,75))
        self.serverBtn.setChecked(True)

        #Client Button
        self.clientBtn = QRadioButton("Client")
        self.clientBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")
        icon = QIcon('images/client.png')
        self.clientBtn.setIcon(icon)
        self.clientBtn.setIconSize(QSize(75,75))

        #Button group to maintain exclusivity
        self.bGroup = QButtonGroup()
        self.bGroup.addButton(self.serverBtn, 1)
        self.bGroup.addButton(self.clientBtn, 2)

        #Next Button
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
        # Server intro message
        self.cIntro = QLabel("Operating as a client")
        self.cIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Server host key & val
        self.cHostKey = QLabel("Host: ")
        self.cHostKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")
        self.cHostVal = QLineEdit()
        self.cHostVal.setPlaceholderText("Say Dell-G3")
        
        # Server port key & val
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
        self.cCIntro =  QtWidgets.QLabel("Operating as a client")
        self.cCIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        self.cConnected = QLabel("Connected!")
        self.cConnected.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # Integrate grid layout
        self.cCLayout = QGridLayout()
        self.cCLayout.addWidget(self.cCIntro, 0,0,1,3)
        self.cCLayout.addWidget(self.cConnected, 1,0,1,3)
        self.stack4.setLayout(self.cCLayout)

    def clientsListUI(self):
        self.stack5.setFixedWidth(500)
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
        
        # Server msg
        self.cLMsg = QLabel("Clients Connected:")
        self.cLMsg.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        self.musicFiles = []
        for f in os.listdir(MUSIC_PATH):
            if os.path.isfile(os.path.join(MUSIC_PATH, f)):
                f = f.lower()
                if f.endswith('.mp3') or f.endswith('.flac') or f.endswith('.aac') or f.endswith('.wav'):
                    self.musicFiles.append(f)

        self.musicBox = QComboBox()
        
        for m in self.musicFiles:
            self.musicBox.addItem(m)
        
        # music helper label
        self.mHelper = QLabel("Select Music")
        self.mHelper.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

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

        # integrate into grid layout
        self.cLLayout = QGridLayout()
        self.cLLayout.addWidget(self.cLIntro, 0,0,1,3)
        self.cLLayout.addWidget(self.cLHostKey, 1,0)
        self.cLLayout.addWidget(self.cLHostVal, 1,1)
        self.cLLayout.addWidget(self.cLPortKey, 2,0)
        self.cLLayout.addWidget(self.cLPortVal, 2,1)
        self.cLLayout.addWidget(self.cLMsg, 3,0,1,3)
        self.clientLabels = []
        for _ in range(self.maxClients):
            self.clientLabels.append(QLabel(""))
        for i,c in enumerate(self.clientLabels):
            self.cLLayout.addWidget(c, 3+(i+1),0,1,3)
        self.cLLayout.addWidget(self.mHelper, self.maxClients+4, 0)
        self.cLLayout.addWidget(self.musicBox, self.maxClients+4, 1, 1, 2)
        self.cLLayout.addWidget(self.playBtn, self.maxClients+5,0)
        self.cLLayout.addWidget(self.pauseBtn, self.maxClients+5,1)
        self.cLLayout.addWidget(self.stopBtn, self.maxClients+5,2)
        self.cLLayout.addWidget(self.endBtn, self.maxClients+6, 1)
        self.stack5.setLayout(self.cLLayout)