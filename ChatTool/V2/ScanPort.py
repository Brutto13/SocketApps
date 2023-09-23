import socket
import datetime
import sys

from colorama import Fore, Back, Style, init

init(True)



logo = '''
 ######   ######     ###    ##    ##    ########   #######  ########  ######## 
##    ## ##    ##   ## ##   ###   ##    ##     ## ##     ## ##     ##    ##    
##       ##        ##   ##  ####  ##    ##     ## ##     ## ##     ##    ##    
 ######  ##       ##     ## ## ## ##    ########  ##     ## ########     ##    
      ## ##       ######### ##  ####    ##        ##     ## ##   ##      ##    
##    ## ##    ## ##     ## ##   ###    ##        ##     ## ##    ##     ##    
 ######   ######  ##     ## ##    ##    ##         #######  ##     ##    ##    
                                                            '''

print(Fore.LIGHTBLUE_EX + logo)
print(Fore.LIGHTBLUE_EX + 'Welcome to this simple port scanning tool.')
print(Fore.YELLOW + 'WARNING!!!: DO NOT SCAN PUBLIC PORTS!\nYOU CAN BE BANNED BY NETWORK OPERATOR!')



target = input('ENTER SCANNED IP: ')

start = int(input('Enter starting scan port: '))
end = int(input('Enter ending scan port: '))

# Add Banner
print("-" * 50)
print(Fore.CYAN + "Scanning Target: " + Fore.YELLOW + target)
print(Fore.CYAN + "Scanning started at:" + Fore.YELLOW + str(datetime.datetime.now()))
print("-" * 50)
  
try:
    for port in range(start, end+1, 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
         
        # returns an error indicator
        result = s.connect_ex((target,port))
        if result ==0:
            print(Fore.CYAN + "Port {} ".format(port) + Fore.GREEN + 'OPEN' + Fore.RESET)
            s.send('<SCAN>'.encode())
        else:
            print(Fore.CYAN + 'Port {} '.format(port) + Fore.RED + 'CLOSED' + Fore.RESET)
        s.close()
    
    print(Fore.LIGHTGREEN_EX + 'SCANNING DONE!')
    input()
         
except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()


