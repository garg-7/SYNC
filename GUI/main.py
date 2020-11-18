from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from _thread import start_new_thread
import time, sys, socket, pygame, os
from PyQt5.QtCore import QRunnable, QThreadPool
from gui import Ui_Main

# PORT = 9077
# MAX_CLIENTS = 2
MUSIC_PATH = 'music'

def sendOpn(clientSocket, cmd):
    clientSocket.send(cmd.encode('UTF-8').strip())

def isEmpty(path):
    for f in os.listdir(path):
        f = f.lower()
        if f.endswith('.mp3') or f.endswith('.flac') or f.endswith('.ogg') or f.endswith('.aac') or f.endswith('.wav'):
            return False
    return True

class Main(QMainWindow, Ui_Main):
    def __init__(self, host, parent=None ):
        super(Main, self).__init__(parent)
        self.clients = []
        self.setupUi(self, host)

        # action to main next button
        self.nextBtn.clicked.connect(self.decideNode)

        # action to the server's next btn
        self.sNextBtn.clicked.connect(self.startServer)

        # action to the connect button on client
        self.cntBtn.clicked.connect(self.attemptConnection)

    def startServer(self):
        self.maxClients = self.sIBox.value()
        self.sPort = self.sIPortVal.value()
        self.finishUI()

        # action to the proceed button on server
        self.proBtn.clicked.connect(self.clientList)

        # action to the verify button on server
        self.vfyBtn.clicked.connect(self.verifyFilePresence)

        # action to the go back button on the server
        self.backBtn.clicked.connect(self.backToClients)

        # action to the play, pause and stop btns
        self.playBtn.clicked.connect(self.play)
        self.pauseBtn.clicked.connect(self.pause)
        self.stopBtn.clicked.connect(self.stop)
        self.endBtn.clicked.connect(self.end)

        self.QtStack.setCurrentIndex(3)
        start_new_thread(self.startListening, ())

    def backToClients(self):
        for c in self.clients:
            start_new_thread(sendOpn, (c[0], 'change'))
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.clientList()

    def verifyFilePresence(self):
        self.songName.setText(self.cFVmusicBox.currentText())
        for i, c in enumerate(self.clients):
            c[0].send(self.cFVmusicBox.currentText().encode())
            resp = c[0].recv(100).decode()
            if resp == 'yes':
                self.filePresence[i].setText(f"{c[1]} already had the file")
                pass
            else:
                self.filePresence[i].setText(f"{c[1]} has received the file")
                f = open(os.path.join(MUSIC_PATH, self.cFVmusicBox.currentText()), 'rb')
                file_content = f.read(110241024)
                c[0].sendall(file_content)
        self.QtStack.setCurrentIndex(6)

    def checkFile(self):
        self.fileToBePlayed = self.cS.recv(1000).decode()
        if os.path.isfile(os.path.join(MUSIC_PATH, self.fileToBePlayed)):
            self.cS.send('yes'.encode())
        else:
            self.cS.send('no'.encode())
            f = open(os.path.join(MUSIC_PATH, self.fileToBePlayed), 'wb')
            file_content = self.cS.recv(110241024)
            f.write(file_content)
            f.close()
        pygame.mixer.music.load(os.path.join(MUSIC_PATH, self.fileToBePlayed))

    def keepReceiving(self):
        # create the music directory if not present
        if not os.path.isdir(MUSIC_PATH):
            os.makedirs(MUSIC_PATH)

        # check if the music to be played is present at the client's end
        self.checkFile()
        while True:
            received = self.cS.recv(200).decode()
            if received == 'play':
                pygame.mixer.music.play()
                print("Starting playback...")
            elif received == 'resume':
                pygame.mixer.music.unpause()
                print("Playback resumed...")
            elif received == 'pause':
                pygame.mixer.music.pause()
                print("Playback paused...")
            elif received == 'stop':
                pygame.mixer.music.stop()
                print("Playback stopped...")
            elif received == 'end':
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                print("## connection closed ##")
                break
            elif received == 'change':
                pygame.mixer.music.stop()
                print("Playback stopped...")
                self.checkFile()

    def play(self):
        if pygame.mixer.music.get_busy():
            for c in self.clients:
                start_new_thread(sendOpn, (c[0], 'resume'))
            # time.sleep(0.25)
            pygame.mixer.music.unpause()
        else:
            for c in self.clients:
                start_new_thread(sendOpn, (c[0], 'play'))
            # time.sleep(0.25)
            pygame.mixer.music.load(os.path.join(MUSIC_PATH, self.cFVmusicBox.currentText()))
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
        
    def end(self):
        for c in self.clients:
            start_new_thread(sendOpn, (c[0], 'end'))
        # time.sleep(0.25)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os._exit(0)

    def clientList(self):
        if len(self.clients)!=0:
            self.QtStack.setCurrentIndex(5)
            for i,c in enumerate(self.clients):
                self.clientLabels[i].setText(f"Connected with {c[1]}, allotted ID={i+1}")

    def attemptConnection(self):
        host = self.cHostVal.text()
        port = int(self.cPortVal.text())
        self.cS = socket.socket()
        self.cS.connect((host, port))
        self.cS.recv(1024)
        self.QtStack.setCurrentIndex(4)
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
        if not os.path.isdir(MUSIC_PATH):
            os.makedirs(MUSIC_PATH)
            self.eMsg.setText("Music folder has been created. Add music to it.")
            self.QtStack.setCurrentIndex(7)
        
        elif isEmpty(MUSIC_PATH):
            self.eMsg.setText("Add some music to the 'music/' folder")
            self.QtStack.setCurrentIndex(7)

        else:
            # listing out files in the music directory
            self.musicFiles = []
            for f in os.listdir(MUSIC_PATH):
                if os.path.isfile(os.path.join(MUSIC_PATH, f)):
                    f = f.lower()
                    if f.endswith('.mp3') or f.endswith('.flac') or f.endswith('.ogg') or f.endswith('.aac') or f.endswith('.wav'):
                        self.musicFiles.append(f)
            self.QtStack.setCurrentIndex(1)

    def client(self):
        self.QtStack.setCurrentIndex(2)


pygame.mixer.init()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    showMain = Main(socket.gethostname())
    sys.exit(app.exec_())