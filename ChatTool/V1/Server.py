import socket
import threading
import json
from colorama import Fore, Back, Style, init

init(True)

json_schema = {
    'host':str,
    'port':int,
    'maxClients':int,
}

# try:
#     file = open('history.log', 'w')
# except:
#     file = open('history.log', 'x')

INFO = Fore.CYAN + '[INFO]: '     # normal info
WARN = Fore.YELLOW + '[WARN]: '   # not good not terrible warning
ERROR = Fore.RED + '[ERROR]: '    # terrible error
FATAL = Style.BRIGHT + Fore.RED + '[FATAL]: '   # like f.e.: ConnectionClosed due to unhandled exception

try:
    with open('server-properties.json', 'r') as file:
        settings = json.loads(file.read())

except:
    print(WARN + 'Config file not detected!')
    ip = input('ENTER IP: ')
    port = input('ENTER PORT: ')
    maxcl = input('ENTER MAXIMUM CLIENT NUMBER: ')
    data = {
        'host':ip,
        'port':port,
        'maxClients':maxcl
    }
    with open('server-properties.json', 'x') as file:
        file.write(json.dumps(data))
        quit()

print(INFO + 'Config.json settings read!')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((settings['host'], int(settings['port'])))
server.listen()



clients = []
nicknames = []

def broadcast(message: str):
    for client in clients:
        client.send(message)

def handle(client: socket.socket, nick):
    while True:
        try:
            message = client.recv(1024)
            if len(message) > 0:
                broadcast(message)
                # file.write(message.decode() + '\n')
                # print(f'Broadcasting {message} from {nick}')
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            if nickname != '<SCAN>':
                broadcast(f"{nickname} left the chat due to unhandled exception!".encode())
                print(f"{ERROR}{nickname} left the chat due to unhandled exception!")
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, addr = server.accept()
        print(INFO + f'Connected with {addr[0]}')
        client.send('<NICK>'.encode())
        nickname = client.recv(1024).decode()
        if nickname != '<SCAN>':
            if len(clients) < int(settings['maxClients']):
                clients.append(client)
                nicknames.append(nickname)
                print(f'SERVER: {nickname} joined the chat! ({len(clients)}/{settings["maxClients"]})')
        
                thread = threading.Thread(
                    target=handle,
                    args=(client,nickname,)
                )
                thread.start()
            else:
                print(Fore.RED + 'REFUSED CONNECTION FROM ADDRESS: ' + addr[0] + ' DUE TO ERROR:\n\rThe chatroom is full and cannot receive one more connection!')
                client.send(f"<REFUSE>".encode())
                client.close()
        else:
            client.close()
    
print(INFO + 'Server is listening on port: ' + Fore.YELLOW + settings['port'])

receive()
# file.close()
