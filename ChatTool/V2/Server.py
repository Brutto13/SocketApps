import tkinter as tk
import socket
import threading
import json


from tkinter.messagebox import *

clients = []
nicknames = []

stopped = False


# except:
#     # print('Config file not detected!')
#     # ip = input('ENTER IP: ')
#     # port = input('ENTER PORT: ')
#     # maxcl = input('ENTER MAXIMUM CLIENT NUMBER: ')
#     # data = {
#     #     'host':ip,
#     #     'port':port,
#     #     'maxClients':maxcl
#     # }
#     # with open('server-properties.json', 'x') as file:
#     #     file.write(json.dumps(data))
#     #     quit()
#     showerror('Server', 'Server properties file not detected!')




window = tk.Tk()
window.title('Chat Server')
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(1, minsize=0, weight=1)

lab_ip = tk.Label(text='IP')
lab_port = tk.Label(text='Port')
lab_max = tk.Label(text='MAX Clients')

frm_buttons = tk.Frame()

width = 55
ent_ip = tk.Entry(width=width)
ent_port= tk.Entry(width=width)
ent_maxcl = tk.Entry(width=width)
ent_message = tk.Entry(frm_buttons, width=width-20)



txt_log = tk.Text(width=width-10, state='disabled')
# txt_clients = tk.Text(frm_buttons, width=width-30, height=15)


try:
    with open('server-properties.json', 'r') as file:
        settings = json.loads(file.read())
        ent_ip.insert(0, settings['host'])
        ent_port.insert(0, settings['port'])
        ent_maxcl.insert(0, settings['maxClients'])
except:
    # showwarning('Server', 'No Config-File detected!')
    pass


def broadcast(message: str):
    for client in clients:
        client.send(message)

def handle(client: socket.socket):
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
                broadcast(f"{nickname} left the chat!".encode())
                txt_log.config(state='normal')
                txt_log.insert(tk.END, f"{nickname} left the chat!\n")
                txt_log.config(state='disabled')
            nicknames.remove(nickname)
            break

def receive():
    global stopped

    while not stopped:
        while True:
            client, addr = server.accept()
            txt_log.insert(tk.END, f'Connected with {addr[0]}\n')
            client.send('<NICK>'.encode())
            nickname = client.recv(1024).decode()
            if nickname != '<SCAN>':
                if len(clients) < int(ent_maxcl.get()):
                    clients.append(client)
                    nicknames.append(nickname)
                    broadcast(f'SERVER: {nickname} joined the chat! ({len(clients)}/{int(ent_maxcl.get())})'.encode())

                    txt_log.config(state='normal')
                    txt_log.insert(tk.END, f'SERVER: {nickname} joined the chat! ({len(clients)}/{ent_maxcl.get()})\n')
                    txt_log.config(state='disabled')

                    thread = threading.Thread(
                        target=handle,
                        args=(client,)
                    )
                    thread.start()
                else:
                    txt_log.config(state='normal')
                    txt_log.insert(tk.END, 'REFUSED CONNECTION FROM ADDRESS: ' + addr[0] + ' DUE TO ERROR:\n\rThe chatroom is full and cannot handle one more connection!')
                    txt_log.config(state='disabled')
                    client.send(f"<REFUSE>".encode())
                    client.close()
            else:
                client.close()

Receive = threading.Thread(
    target=receive,
    name='Server-RECV'
)
def lockEntrys():
    ent_ip.config(state='readonly')
    ent_port.config(state='readonly')
    ent_maxcl.config(state='readonly')
    btn_start.config(state='disabled')

def unlockEntrys():
    ent_ip.config(state='normal')
    ent_port.config(state='normal')
    ent_maxcl.config(state='normal')
    btn_start.config(state='normal')

def start():
    try:
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ent_ip.get(), int(ent_port.get())))
        server.listen()
        Receive.start()
        lockEntrys()
        showinfo('Server', f'Server hosted on {ent_ip.get()}:{ent_port.get()} succesfully!')
    except:
        showerror('Server', 'ValueError: Wrong or occupied port/IP number!')



def stop():    
    if askokcancel('Server', 'Closing server will disconnect all clients.\nAre you sure you want to do this?'):
        for client in clients:
            client.close()
        
        showinfo('Server', 'Server closed succesfully!')

def SendMessage():
    try:
        message = f"ADMIN: {ent_message.get()}".encode()
        broadcast(message)
        ent_message.delete(0, tk.END)
    except Exception as e:
        showerror('Client', f'ERROR: {e}')



btn_start = tk.Button(frm_buttons, text='Start Server', width=35, command=start)
btn_stop = tk.Button(frm_buttons, text='Stop Server', width=35, command=stop)
btn_send = tk.Button(frm_buttons, text='Send', command=SendMessage, width=35)


# packaging
lab_ip.grid(row=0, column=0, padx=5, pady=5)
ent_ip.grid(row=0, column=1, padx=5, pady=5)

lab_port.grid(row=1, column=0, padx=5, pady=5)
ent_port.grid(row=1, column=1, padx=5, pady=5)

lab_max.grid(row=2, column=0, padx=5, pady=5)
ent_maxcl.grid(row=2, column=1, padx=5, pady=5)

###################################################
frm_buttons.grid(row=3, column=0, padx=5, pady=5, sticky='n')
btn_start.grid(row=0, column=0, padx=5, pady=5)
btn_stop.grid(row=1, column=0, padx=5, pady=5)
btn_send.grid(row=3, column=0, padx=5, pady=5)
ent_message.grid(row=4, column=0, padx=5, pady=5)
# txt_clients.grid(row=5, column=0)
###################################################

txt_log.grid(row=3, column=1, padx=5, pady=5)

window.mainloop()