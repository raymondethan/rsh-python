from socket import *
import os.path, time
import threading

def send(*args):
    ip = "".join(args)
    print(ip)
    #last_modified = None
    port = 55567
    buf = 1024

    #while True:
    # try:
    #     modified = time.ctime(os.stat(filename).st_mtime)
    # except Exception:
    #     continue
    #If file is modified, sends contents of file to all servers in list of IP addresses
    #if (not last_modified or last_modified < modified):
        # last_modified = modified
        # data = readfile(filename)
        #for ip in IPS:
    login = input(">>> Password: ")
    cmd = str(login)
    print("Command: " + cmd)
    addr = (ip, port)
    while 'exit' != cmd:
        try:
            clientsocket = socket(AF_INET, SOCK_STREAM)
            clientsocket.connect(addr)
            #socket module only accepts data in bytes
            clientsocket.send(cmd.encode('ascii'))
            response = clientsocket.recv(1024).decode('ascii')
            if response:
                print(response)
            clientsocket.close()
        except Exception as e:
            print("Send exception: ",e)
        cmd = input(">>> ")


def main():
    print("RSH\n")
    ip = input("RSH Address: ")
    #send login info
    #if response is positive
    #while loop until exit is typed
    sender = threading.Thread(target=send,name="Sender",args=(ip))
    #receiver = threading.Thread(target=receive,name="Receiver")
    #receiver.start()
    sender.start()

if __name__ == "__main__":
    main()