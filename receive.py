from socket import *
import os.path, time
from os import fork, execvp, waitpid
from sys import exit
import threading

login = False

def handler(clientsocket, clientaddr):
    global login
    password = "pats"
    while True:
        data = clientsocket.recv(1024).decode('ascii')
        if not data:
            break
        if not login:
            if data == password:
                login = True
                clientsocket.send("Authentication successful".encode('ascii'))
            else:
                clientsocket.send("Authentication failed. Please reenter password".encode('ascii'))
        else:
            try:
                try:
                    cmd = str(data).split()
                    status = int()
                    pid = fork()
                    if pid < 0:
                        raise Exception("fork failed")
                    elif 0 == pid:
                        try:
                            print("Inside child process\n")
                            print("Command output\n")
                            execvp(cmd[0],cmd)
                            print("Exec failed\n")
                            exit(1)
                        except Exception as e:
                            print("child process exception: ",e)
                    else:
                        try:
                            x, stat = waitpid(pid, status)
                            if x < 0:
                                print("Child error")
                            else:
                                print("Child executed successfully")
                        except Exception as e:
                            print("Parent process exception: ",e)
                    clientsocket.send("Command executed".encode('ascii'))
                except Exception as e:
                    print("Failed to parse command: ",e)
                    break
            except Exception as e:
                print("Handler exception: ",e)
    clientsocket.close()

#I need this method if I want to be able to accept multiple senders at once
#Is this the behavior that RSH should implement?
def receive():
    port = 55567
    buf = 1024

    addr = ('', port)

    serversocket = socket(AF_INET, SOCK_STREAM)

    serversocket.bind(addr)

    serversocket.listen(1)

    while True:
        clientsocket, clientaddr = serversocket.accept()
        thread = threading.Thread(target=handler, args=(clientsocket, clientaddr))
        thread.start()
    serversocket.close()

def main():
    #print("RSH\n")
    #ip = input("RSH Address: ")
    #send login info
    #if response is positive
    #while loop until exit is typed
    #sender = threading.Thread(target=send,name="Sender",args=(ip))
    receiver = threading.Thread(target=receive,name="Receiver")
    receiver.start()
    #sender.start()

if __name__ == "__main__":
    main()