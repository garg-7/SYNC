from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from _thread import start_new_thread
import time, sys, socket, pygame, os
from PyQt5.QtCore import QRunnable, QThreadPool
from f import Ui_Main

PORT = 9077
MAX_CLIENTS = 2
MUSIC_PATH = 'music'

def sendOpn(clientSocket, cmd):
    clientSocket.send(cmd.encode())

class Main(QMainWindow, Ui_Main):
    def __init__(self, host, port, maxClients, parent=None ):
        self.clients = []
        super(Main, self).__init__(parent)
        self.setupUi(self, host, port, maxClients)

        # action to main next button
        self.nextBtn.clicked.connect(self.decideNode)

        # action to the proceed button on server
        self.proBtn.clicked.connect(self.player)

        # action to the play, pause and stop btns
        self.playBtn.clicked.connect(self.play)
        self.pauseBtn.clicked.connect(self.pause)
        self.stopBtn.clicked.connect(self.stop)
        self.endBtn.clicked.connect(self.end)

        # action to the connect button on client
        self.cntBtn.clicked.connect(self.attemptConnection)


    def play(self):
        if pygame.mixer.music.get_busy():
            for c in self.clients:
                start_new_thread(sendOpn, (c[0], 'play'))
            # time.sleep(0.25)
            pygame.mixer.music.unpause()
        else:
            for c in self.clients:
                start_new_thread(sendOpn, (c[0], 'play_'+self.musicBox.currentText()))
            # time.sleep(0.25)
            pygame.mixer.music.load(MUSIC_PATH+'/'+self.musicBox.currentText())
            pygame.mixer.music.play()

    def pause(self):
        for c in self.clients:
            start_new_thread(sendOpn, (c[0], 'pause'))
        # time.sleep(0.25)
        pygame.mixer.music.pause()

    def stop(self):
        for c in self.clients:
            start_new_thread(sendOpn, (c[0], 'stop'))
        # time.sleep(0.25)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        
    def end(self):
        for c in self.clients:
            start_new_thread(sendOpn, (c[0], 'end'))
        # time.sleep(0.25)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os._exit(0)

    def player(self):
        if len(self.clients)!=0:
            self.QtStack.setCurrentIndex(4)
            for i,c in enumerate(self.clients):
                self.clientLabels[i].setText(f"Connected with {c[1]}, allotted ID={i+1}")

    def keepReceiving(self):
        while True:
            received = self.cS.recv(200).decode()
            if received.startswith('play'):
                if '_' in received:
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(MUSIC_PATH+'/'+received.split('_')[1])
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.unpause()
                print("Starting playback...")
            elif received == 'pause':
                pygame.mixer.music.pause()
                print("Playback paused...")
            elif received == 'stop':
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                print("Playback stopped...")
            elif received == 'end':
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                print("## connection closed ##")
                os._exit(0)
                break

    def attemptConnection(self):
        host = self.cHostVal.text()
        port = int(self.cPortVal.text())
        self.cS = socket.socket()
        self.cS.connect((host, port))
        self.cS.recv(1024)
        self.QtStack.setCurrentIndex(3)
        start_new_thread(self.keepReceiving, ())

    def decideNode(self):
        # print(self.bGroup.checkedId())
        if self.bGroup.checkedId()==1:
            self.server()
        elif self.bGroup.checkedId()==2:
            self.client()

    def startListening(self):
        s = socket.socket()
        s.bind((self.sHost,self.sPort))
        s.listen()
        ID = 0
        while ID<self.maxClients:
            clientsocket, address = s.accept()
            self.clients.append((clientsocket, address))
            ID+=1
            clientsocket.send('Welcome!'.encode())
        return

    def server(self):
        self.QtStack.setCurrentIndex(1)
        start_new_thread(self.startListening, ())

    def client(self):
        self.QtStack.setCurrentIndex(2)


pygame.mixer.init()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    showMain = Main(socket.gethostname(), PORT, MAX_CLIENTS)
    sys.exit(app.exec_())