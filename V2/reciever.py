from datetime import date
import os
import socket
# from tkinter.ttk import Progressbar
# import tqdm
# import alive_progress
import base64
import hashlib
import json
from colorama import Fore, Style, init
from maximize import maximize_console
import progressBar

maximize_console()
logo = '''
____                    __              __      
/\  _`\                 /\ \            /\ \__   
\ \,\L\_\    ___     ___\ \ \/'\      __\ \ ,_\  
 \/_\__ \   / __`\  /'___\ \ , <    /'__`\ \ \/  
   /\ \L\ \/\ \L\ \/\ \__/\ \ \\\\`\ /\  __/\ \ \_ 
   \ `\____\ \____/\ \____\\\\ \_\ \_\ \____\\\\ \__\\
    \/_____/\/___/  \/____/ \/_/\/_/\/____/ \/__/

                                               
 ______                                 ___               
/\__  _\                              /'___\              
\/_/\ \/ _ __    __      ___     ____/\ \__/   __   _ __  
   \ \ \/\`'__\/'__`\  /' _ `\  /',__\ \ ,__\/'__`\/\`'__\\
    \ \ \ \ \//\ \L\.\_/\ \/\ \/\__, `\ \ \_/\  __/\ \ \/ 
     \ \_\ \_\\ \__/.\_\ \_\ \_\/\____/\ \_\\ \____\\ \_\ 
      \/_/\/_/ \/__/\/_/\/_/\/_/\/___/  \/_/ \/____/ \/_/ 
'''

print(Fore.GREEN + logo)

json_schema = {
    'socket':{
        'defIP':str,
        'defPort':int
    },
    'whitelist':list[str],
    'autoDownload':list[str],
    'path':str
}

# socket - default socket settings
# whitelist - list of IPs that has no warnings
# autoDownload - list of senders whos files are downloaded automaticly

# first-run config
try:
    config = open('config.json', 'r')
    content = config.read()
    settings = json.loads(content)
    config.close()
        
except:
    print(Fore.YELLOW + '[WARN]: No config file detected!')
    IP = input('Enter default IP: ')
    PORT = input('Enter default port: ')
    
    print('Enter whitelist IPs (those IPs without warnings; type \"!\" to end adding)')
    whitelist = []
    done = False
    while not done:
        ip = input('$ ')
        if ip != '!':
            whitelist.append(ip)
        else: done = True
    
    print('Enter IPs fromwhat files will be automaticly downloaded ' + Fore.YELLOW + 'WARNING! PROCEED WITH CAUTION')
    autoDownloads = []
    done = False
    while not done:
        ip = input('$ ')
        if ip != '!':
            autoDownloads.append(ip)
        else: done = True
    
    path = input('Enter output path (received files goes there): ')

    data = {
        'socket':{
            'defIP':IP,
            'defPort':int(PORT)
        },
        'whitelist':whitelist,
        'autoDownload':autoDownloads,
        'path':path
    }

    with open('config.json', 'x') as file:
        settings = data
        file.write(json.dumps(data))
        del data
        input('PLEASE NOW RESTART THE PROGRAM')
        quit()

init(True)

CYAN = Fore.CYAN
YELLOW = Fore.YELLOW

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ipadress = input('[INPUT]: Enter your IP address: ')
# port = input('[INPUT]: Enter port: ')
# mode = input('[INPUT]: Do you expect text (T) or bytes (B): ')

Y = 'Y'.encode()
N = 'N'.encode()

IP = settings['socket']['defIP']
PORT = settings['socket']['defPort']

print(CYAN + '[INFO]: check settings:')
print(CYAN + 'Your IP address: ' + Fore.GREEN + IP)
print(CYAN + 'Your port: ' + Fore.GREEN + str(PORT))
print(CYAN + 'Destination path: ' + Fore.GREEN + settings['path'])
print(YELLOW + 'IF YOU WANT TO CHANGE THOSE SETTINGS DELETE THE \"config.json\" FILE!')

server.bind((IP, PORT))
print(CYAN + '[INFO]: Awaiting for transmitter side...')
while True:
    server.listen()
    client, addr = server.accept()

    file_name = client.recv(1024).decode()
    file_size = client.recv(1024).decode()
    md5sum = client.recv(1024).decode()
    description = client.recv(1024).decode()
    SenderIP = addr[0]
    # md5sum = client.recv(1024).decode()
    file_size = int(file_size)
    # if file_size < 10**3:
    #     unit = 'kB'
    #     file_size = file_size/10**3
    
    # elif file_size > 10**3:
    #     unit = 'MB'
    #     file_size = file_size / 10**3

    # elif file_size < 1000:
    #     unit = 'B'

    print(CYAN + 'Sender: ' + YELLOW + addr[0])
    print(CYAN + 'File name: ' + YELLOW + file_name)
    print(CYAN + 'File size: ' + YELLOW + str(file_size) + 'B')
    print(CYAN + 'output file destination: ' + YELLOW + (os.getcwd() + '\\' + file_name))
    print(CYAN + 'Description: ' + YELLOW + description)
    

    file_size = str(file_size)
    speed = 16384
    file_bytes = b""
    print(CYAN + 'Speed: ' + YELLOW + str(speed) + 'B/i')

    done = False
    status = 0
    # progress = tqdm.tqdm(unit=unit, unit_divisor=1000000, unit_scale=1, total=float(file_size), colour='green')
    # progress = Bar('Downloading... ', suffix='%(percent).1f%% - %(eta)ds')
    # oneOfThundred = (int(file_size)/1000)/100
    # progress = tqdm.tqdm(unit='B', unit_scale=True, unit_divisor=1000, total=float(file_size), colour='green')
    # progress = alive_progress.alive_bar(total=int(file_size), title='Processing... ', manual=True)
    progress = progressBar.ProgressBar(
        name='Downloading File...',
        total=int(file_size),
        divisor=int(file_size)//100,
        color=Fore.GREEN,
    )
    while not done:
        # old = len(file_bytes)
        data = client.recv(speed)
        if data[-8:] == b'!End:...':
            # print(data[:-8])
            file_bytes += data[:-8]
            done = True
        else: file_bytes += data
        # status = len(file_bytes)
        
        # new = status - old
        progress.plot()
        progress.add(speed)
        
        


        


    print(CYAN + '\n[INFO]: file received succesfully')
    # print(file_bytes)
    data = base64.b64decode(file_bytes)
    file = open((settings['path'] + '\\' + file_name), 'wb')
    file.write(data)
    file.close()
    
    
    # md5sum check, if equals to expected closes the file and waits
    # for new connection, otherwise deletes file.
    # file = open(os.getcwd() + file_name, 'rb')
    # content = file.read()
    read_file = open((settings['path'] + '\\' + file_name), 'rb')
    read_file_size = os.path.getsize(settings['path'] + '\\' + file_name)
    read_data = read_file.read()
    recvKey = hashlib.md5(read_data).hexdigest()
    if not md5sum == recvKey:
        print(Fore.RED + '[ERROR]: ConnectionError: Received file is incomplete or damaged\nAsk sender for new one.')
        print(md5sum)
        print(recvKey)
        print(read_file_size)
        client.send('ERROR'.encode())
        # input()
        # quit()
    else:
        client.send('OK'.encode())
    # file = open((os.getcwd() + '\\' + file_name), 'wb')
    # file.write(data)

    # file.close()
    client.close()

    print(Fore.GREEN + '[EXIT]: Operation Done!')
    print('STATS:')
    print(CYAN + 'Iteration speed [iterations/second]: ' + YELLOW + str(round(int(file_size)/speed, 1)) + 'i/s')
    

    print(CYAN + '[INFO]: Awaiting for new file, close console to abort...')
    print(Style.BRIGHT + '=====================================================')
