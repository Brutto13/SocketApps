import socket
import threading

from tkinter import *
from tkinter.messagebox import *

# client = ...

window = Tk()
window.title('ChatTool Client GUI v2')
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(1, minsize=0, weight=1)

frm_BigFrame = Frame()
frm_data = Frame(frm_BigFrame)
frm_buttons = Frame(frm_BigFrame)
frm_text = Frame()

lab_ip = Label(frm_data, text='IP')
lab_port = Label(frm_data, text='Port')
lab_nick = Label(frm_data, text='Nickname')

width = 20
ent_ip = Entry(frm_data, width=width)
ent_port = Entry(frm_data, width=width)
ent_nick = Entry(frm_data, width=width)
ent_message = Entry(frm_text, width=53)

txt_Chat = Text(frm_text, width=40, state='disabled')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def lockEntrys():
    ent_ip.config(state='readonly')
    ent_port.config(state='readonly')
    ent_nick.config(state='readonly')
    btn_connect.config(state='disabled')

def unlockEntrys():
    ent_ip.config(state='normal')
    ent_port.config(state='normal')
    ent_nick.config(state='normal')
    btn_connect.config(state='normal')

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == '<NICK>':
                client.send(ent_nick.get().encode())
            
            elif message == '<REFUSED>':
                showerror('Client', 'Server refused connection!')
                client.close()
                quit()
            
            elif message == '<CLOSE>':
                client.close()
                showerror("Client", "Server closed the connection")
                txt_Chat.config(state='normal')
                txt_Chat.delete("0.0", END)
                txt_Chat.config(state='disabled')
                btn_leave.config(state='disabled')
                btn_send.config(state='disabled')
                btn_connect.config(state='normal')
                unlockEntrys()
            

            else:
                # (message)
                txt_Chat.config(state='normal')
                txt_Chat.insert(END, message + '\n')
                txt_Chat.config(state='disabled')
        except Exception as e:
            print(e)
            client.close()
            break

def write():
    message = f"{ent_nick.get()}:{ent_message.get()}".encode()
    client.send(message)
    ent_message.delete(0, END)

def leave():
    if askyesno("Client", "Are you sure you wish to leave this chatroom?"):
        client.close()
        # quit()
        
        unlockEntrys()
        # quit()
        txt_Chat.config(state='normal')
        txt_Chat.delete("0.0", END)
        txt_Chat.config(state='disabled')
        btn_leave.config(state='disabled')
        btn_send.config(state='disabled')
        btn_connect.config(state='normal')
        showinfo("Client", "Chatroom left succesfully")


Recv = threading.Thread(target=receive)

def ConnectToServer():
    done = False
    while not done:
        try:
            client.connect((ent_ip.get(), int(ent_port.get())))
            lockEntrys()
            showinfo('Client', f'Connected to {ent_ip.get()}:{ent_port.get()}')
            Recv.start()
            btn_leave.config(state='normal')
            btn_send.config(state='normal')
            btn_connect.config(state='disabled')
            return
        except socket.gaierror:
            if askretrycancel("Client", f"{ent_ip.get()}:{ent_port.get()} Not responding"):
                done = False
            else:
                done = True
        
        except Exception as e:
            showerror("Client - Fatal Error", "A fatal error occured:\n%s" % e)
            done = True




btn_connect = Button(frm_buttons, text='Connect', command=ConnectToServer, width=25)
btn_leave = Button(frm_buttons, text='Leave', command=leave, width=25, state='disabled')
btn_send = Button(frm_buttons, text='Send', command=write, width=25, state='disabled')

# grid

frm_BigFrame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

####################################################
frm_data.grid(row=0, column=0, padx=5, pady=5, sticky='n')
lab_ip.grid(row=0, column=0, padx=5, pady=5)
lab_port.grid(row=1, column=0, padx=5, pady=5)
lab_nick.grid(row=2, column=0, padx=5, pady=5)
ent_ip.grid(row=0, column=1, padx=5, pady=5)
ent_port.grid(row=1, column=1, padx=5, pady=5)
ent_nick.grid(row=2, column=1, padx=5, pady=5)
####################################################

######################################################################
frm_buttons.grid(row=1, column=0, padx=5, pady=5, sticky='n')
btn_connect.grid(row=0, column=0, padx=5, pady=5)
btn_leave.grid(row=1, column=0, padx=5, pady=5)
btn_send.grid(row=2, column=0, padx=5, pady=5)
######################################################################

######################################################
frm_text.grid(row=0, column=1, padx=5, pady=5)
txt_Chat.grid(row=0, column=0, padx=5, pady=5)
ent_message.grid(row=1, column=0, padx=5, pady=5)

window.mainloop()