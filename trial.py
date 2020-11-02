import socket
import os
import os.path
from os.path import join as pjoin
def send():
    global host
    global port
    global s
    global File_path
    #creating the socket
    s=socket.socket()
    hostname=socket.gethostname()
    ip=socket.gethostbyname(hostname)
    print("Your sharing IP: ", ip)
    #portnumber
    port=9999
    #get host name
    host=""
    #binding the  connection
    s.bind((host,port))
    print("waiting for connection............")
    s.listen(1)
    #establishing the connection
    try:
        c,addr=s.accept()
        print("Connection establish with",addr)
    except socket.error as msg:
        print("Establishing connection check ip enter by client :",msg)
    # Open a file
    File=str(input("Enter the file name to be send:- "))
    try:
        for root,dirs,files in os.walk("c:\\"):
            for files in files:
                if files == File:
                    File_path=os.path.join(root,files)
        print("Your file Location",File_path)
        print(f"Your file size:- {os.path.getsize(File_path)*(1/1048576)}MB")
        fo =open(File_path,"rb")
        content= fo.read(2155639160)
        c.send(content)
        print("File has been send")
        # Close opend file
        fo.close()
        s.close()            
    except:
        try:
            for root,dirs,files in os.walk("d:\\"):
                for files in files:
                    if files ==File:
                        File_path=os.path.join(root,files)
            print("Your file Location",File_path)
            print(f"Your file size:- {os.path.getsize(File_path)*(1/1048576)}MB")
            fo =open(File_path,"rb")
            content= fo.read(21555639160)
            c.send(content)
            print("File has been send")
            # Close opend file
            fo.close()
            s.close()
        except:
            try:
                for root,dirs,files in os.walk("g:\\"):
                    for files in files:
                        if files ==File:
                            File_path=os.path.join(root,files)
                print("Your file Location",File_path)
                print(f"Your file size:- {os.path.getsize(File_path)*(1/1048576)}MB")
                fo =open(File_path,"rb")
                content= fo.read(21555639160)
                c.send(content)
                print("File has been send")
                # Close opend file
                fo.close()
                s.close()
            except:
                try:
                    for root,dirs,files in os.walk("f:\\"):
                        for files in files:
                            if files ==File:
                                File_path=os.path.join(root,files)
                    print("Your file Location",File_path)
                    print(f"Your file size:- {os.path.getsize(File_path)*(1/1048576)}MB")
                    fo =open(File_path,"rb")
                    content= fo.read(21555639160)
                    c.send(content)
                    print("File has been send")
                    # Close opend file
                    fo.close()
                    s.close()
                except:
                    try:
                        for root,dirs,files in os.walk("e:\\"):
                            for files in files:
                                if files ==File:
                                    File_path=os.path.join(root,files)
                        print("Your file Location",File_path)
                        print(f"Your file size:- {os.path.getsize(File_path)*(1/1048576)}MB")
                        fo =open(File_path,"rb")
                        content= fo.read(21555639160)
                        c.send(content)
                        print("File has been send")
                        # Close opend file
                        fo.close()
                        s.close()
                    except:
                        print("we send the files only available on disk:C:,D:,E:,F:,G:")
#to receve the file
def recv():
    global host
    global port
    global s
    s=socket.socket()
    #get hostname on receiver side
    try:
        hostname=str(input("Sender Sharing Ip:- "))
        host=hostname
        port=9999
        s.connect((host,port))
        print("Connecting.......")
    except socket.error as msg:
        print("Check ip you enter",msg)
    filename =input("Enter the file name with extension:-   ")
    recv=s.recv(21555639160)
    file_path =pjoin("C:\\","Users","Kartik Vyas","Downloads",filename)
    print("Your Received File is in:- ",file_path)
    fo = open(file_path, "wb")
    fo.write(recv)
    print("file Received")
    print(f"Your file size:- {os.path.getsize(file_path)*(1/1048576)}MB")
    # Close opend file
    fo.close()
def choose():
    print("Welcome To We Share")
    print("1. Send")
    print("2. recv")
    print("3. Exit")
    press=int(float(input("Chosse 1 or 2 or 3:- ")))
    if(press==1):
        send()
    elif(press==2):
        recv()
    elif(press==3):
        exit()
    else:
        print("sorry we haven't provide any  other features")
def main():
    choose()
    p=int(float(input("press 3 to exit")))
    if(p==3):
        exit()
    else:
        print("Invalid input to Exit")

main()