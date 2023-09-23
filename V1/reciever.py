from datetime import date
import os
import socket
# import tqdm
import base64
import hashlib
from colorama import Fore, Style, init

init(True)

CYAN = Fore.CYAN
YELLOW = Fore.YELLOW

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Ipadress = input('[INPUT]: Enter your IP address: ')
port = input('[INPUT]: Enter port: ')
# mode = input('[INPUT]: Do you expect text (T) or bytes (B): ')

server.bind((Ipadress, int(port)))
print('[INFO]: Awaiting for transmitter side...')
while True:
    server.listen()
    client, addr = server.accept()

    file_name = client.recv(1024).decode()
    file_size = client.recv(1024).decode()
    md5sum = client.recv(1024).decode()
    # md5sum = client.recv(1024).decode()
    print(CYAN + f'[INFO]: {addr[0]} has connected')
    print(CYAN + 'Sender: ' + YELLOW + addr[0])
    print(CYAN + 'File name: ' + YELLOW + file_name)
    print(CYAN + 'File size: ' + YELLOW + file_size + 'B')
    print(CYAN + 'output file destination: ' + YELLOW + (os.getcwd() + '\\' + file_name))
    print(CYAN + 'Expected md5sum: ' + YELLOW + md5sum)


    
    file_bytes = b""

    done = False
    status = 0
    # progress = tqdm.tqdm(unit='B', unit_scale=True, unit_divisor=int(file_size)/100, total=int(file_size), colour='green')
    while not done:
        data = client.recv(1024)
        if data[-8:] == b'!End:...':
            # print(data[:-8])
            file_bytes += data[:-8]
            done = True
        else: file_bytes += data
        status += 1024
        print(CYAN + '[INFO]: Receiving data:%s %s/%s B' % (YELLOW, status, file_size), end='\r')



    print(CYAN + '\n[INFO]: file received succesfully')
    # print(file_bytes)
    data = base64.b64decode(file_bytes)
    file = open((os.getcwd() + '\\' + file_name), 'wb')
    file.write(data)
    file.close()
    
    # md5sum check, if equals to expected closes the file and waits
    # for new connection, otherwise deletes file.
    # file = open(os.getcwd() + file_name, 'rb')
    # content = file.read()
    read_file = open((os.getcwd() + '\\' + file_name), 'rb')
    read_file_size = os.path.getsize(os.getcwd() + '\\' + file_name)
    read_data = read_file.read()
    recvKey = hashlib.md5(read_data).hexdigest()
    if not md5sum == recvKey:
        print(Fore.RED + '[ERROR]: ConnectionError: Received file is incomplete or damaged\nAsk sender for new one.')
        print(md5sum)
        print(recvKey)
        print(read_file_size)
        # input()
        # quit()
    else: pass
    # file = open((os.getcwd() + '\\' + file_name), 'wb')
    # file.write(data)

    # file.close()
    client.close()

    print(Fore.GREEN + '[EXIT]: Operation Done!')
    print(CYAN + '[INFO]: Awaiting for new file, close console to abort...')
    print(Style.BRIGHT + '=====================================================')
