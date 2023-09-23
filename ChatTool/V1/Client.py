import socket
import threading

ip = input('Enter host\'s IP: ')
port = int(input('Enter host\'s PORT: '))
nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, int(port)))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == '<NICK>':
                client.send(nickname.encode())
            
            elif message == '<REFUSED>':
                print('Server refused connection')
                client.close()
                input()
                quit()
            

            else:
                print(message)
        except Exception as e:
            print(e)
            client.close()
            break

def write():
    while True:
        message = f"{nickname}:{input()}"
        client.send(message.encode())


recv = threading.Thread(target=receive)
transmit = threading.Thread(target=write)

recv.start()
transmit.start()