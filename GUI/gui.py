from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QPushButton, QLineEdit, QButtonGroup, QComboBox, QSpinBox
from PyQt5.QtWidgets import QGridLayout, QStackedLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os

MUSIC_PATH = 'music'
class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main, host):
        Main.setObjectName("Main")
        self.sHost = host               # host name of server
        # self.sPort = port               # port at which server accepts connections
        self.maxClients = 0    # max number of clients to connect with the server
        self.QtStack = QStackedLayout()

        self.stack0 = QWidget()   # the main screen
        self.stack1 = QWidget()   # server port and clients entry
        self.stack2 = QWidget()   # client enter info
        self.stack3 = QWidget()   # client connected
        self.stack4 = QWidget()   # server proceed btn display
        self.stack5 = QWidget()   # server music select
        self.stack6 = QWidget()   # server player
        self.stack7 = QWidget()   # error window

        # initialize UI windows
        self.startUI()
        self.serverInit()
        self.clientUI()
        self.clientConnectedUI()
        self.errorDisp()

        # add UI windows to Qt Stack
        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)
        self.QtStack.addWidget(self.stack7)
        
        
    def finishUI(self):
        # initialize remaining UI windows
        self.serverUI(self.sHost, self.sPort)
        self.clientsFileVerify()
        self.clientsListUI()
        return

    def startUI(self):
        self.stack0.setFixedSize(500,200)
        self.stack0.setWindowTitle("Sync")
        
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
        self.stack0.setLayout(self.layout)
        return

    def serverInit(self):
        self.stack1.setFixedSize(500,200)
        self.stack1.setWindowTitle("Sync")
        
        # Server intro message
        self.sIIntro = QLabel("Operating as a server")
        self.sIIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")

        # port helper
        self.sIPortKey = QLabel("Port to listen on: ")
        self.sIPortKey.setStyleSheet("font-size: 20px; qproperty-alignment: AlignLeft; font-family: Helvetica, Arial")

        # port helper
        self.sIPortVal = QSpinBox()
        self.sIPortVal.setValue(9077)
        self.sIPortVal.setMaximum(65535)
        self.sIPortVal.setMinimum(1024)

        # helper label
        self.sIHelper = QLabel("Number of clients: ")
        self.sIHelper.setStyleSheet("font-size: 20px; qproperty-alignment: AlignLeft; font-family: Helvetica, Arial")

        # text field for number of clients
        self.sIBox = QSpinBox()
        self.sIBox.setValue(2)
        self.sIBox.setMaximum(16)
        self.sIBox.setMinimum(1)

        # next Btn
        self.sNextBtn = QPushButton("Next")
        self.sNextBtn.setStyleSheet("font-size: 14px; font-family: Helvetica, Arial")

        # Integrate grid layout
        self.sILayout = QGridLayout()
        self.sILayout.addWidget(self.sIIntro, 0,0,1,3)
        self.sILayout.addWidget(self.sIPortKey, 1,0,1,2)
        self.sILayout.addWidget(self.sIPortVal, 1,1,1,2)
        self.sILayout.addWidget(self.sIHelper, 2,0,1,2)
        self.sILayout.addWidget(self.sIBox, 2,1,1,2)
        self.sILayout.addWidget(self.sNextBtn, 3,1)
        self.stack1.setLayout(self.sILayout)
        return

    def clientUI(self):
        self.stack2.setFixedSize(500,200)
        self.stack2.setWindowTitle("Sync")
        
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
        self.stack2.setLayout(self.cLayout)
        return

    def serverUI(self, host, port):
        self.stack3.setFixedSize(500,200)
        self.stack3.setWindowTitle("Sync")
        
        # Server intro message
        self.sIntro = QLabel("Operating as a server")
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
        self.stack3.setLayout(self.sLayout)
        return

    def clientConnectedUI(self):
        self.stack4.setFixedSize(500,200)
        self.stack4.setWindowTitle("Sync")

        # client intro message
        self.cCIntro =  QLabel("Operating as a client")
        self.cCIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")
        
        # Client welcome msg
        self.cConnected = QLabel("Connected!")
        self.cConnected.setStyleSheet("font-size: 20px; qproperty-alignment: AlignHCenter; font-family: Helvetica, Arial")

        # Integrate grid layout
        self.cCLayout = QGridLayout()
        self.cCLayout.addWidget(self.cCIntro, 0,0,1,3)
        self.cCLayout.addWidget(self.cConnected, 1,0,1,3)
        self.stack4.setLayout(self.cCLayout)
        return

    def clientsFileVerify(self):
        self.stack5.setFixedWidth(500)
        self.stack5.setWindowTitle("Sync")
        
        # Server intro message
        self.cFVIntro = QLabel("Operating as a server")
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
        return

    def clientsListUI(self):
        self.stack6.setFixedWidth(500)
        self.stack6.setWindowTitle("Sync")
        
        # Server intro message
        self.cLIntro = QLabel("Operating as a server")
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

        return

    def errorDisp(self):
        self.stack7.setFixedWidth(500)
        self.stack7.setWindowTitle("Sync")
        
        # Server intro message
        self.eIntro = QLabel("Operating as a server")
        self.eIntro.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")

        # Server intro message
        self.eMsg = QLabel()
        self.eMsg.setStyleSheet("font-size: 20px; qproperty-alignment: AlignCenter; font-family: Helvetica, Arial")

        self.eLayout = QGridLayout()
        self.eLayout.addWidget(self.eIntro, 0,0,1,3)
        self.eLayout.addWidget(self.eMsg, 1,0,1,3)
        self.stack7.setLayout(self.eLayout)
        return