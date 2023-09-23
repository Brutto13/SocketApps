import os, time, base64
from tkinter import *
from tkinter.messagebox import showinfo, showwarning, showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
import socket
import hashlib

from numpy import empty, pad

# sys.stdout = open('transmitting.log')



window = Tk()
window.resizable(False, False)
window.title('Socket File Transmitter Tool V2')
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(1, minsize=1, weight=1)
# window.config()

# current_extension = tk.StringVar()

mode = ('binary', 'text')
current_extension = StringVar()

lab_targetIP = Label(text='Target IP')
lab_port = Label(text='port')
lab_filepath = Label(text='filepath')
lab_targetfilename = Label(text='Target filename')
lab_extension = Label(text='Transmitter mode')
lab_description = Label(text='Description')
# lab_noExtension = Label(text="WARNING Put filename WITHOUT it's extension", fg='red')

# cmb_selectMODE = Combobox(window, values=mode, width=72)

emptyDesc = IntVar(value=0)

chk_empty = Checkbutton(variable=emptyDesc, text='empty')

WIDTH = 75

ent_IP = Entry(width=WIDTH)
ent_port = Entry(width=WIDTH)
ent_filepath = Entry(width=WIDTH)
ent_filename = Entry(width=WIDTH)
ent_descp = Entry(width=WIDTH)

frm_buttons = Frame()

txt_log = Text()

# definitions

def browseCommand():
    filepath = askopenfilename(
        filetypes=[('All Files', '*.*')]
    )
    ent_filepath.delete(0, END)
    ent_filepath.insert(0, filepath)

def SendFileCommand():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ent_IP.get(), int(ent_port.get())))
    file = open(ent_filepath.get(), 'rb')
    file_size = os.path.getsize(ent_filepath.get())
    data = file.read()
    print(file_size)
    client.send(ent_filename.get().encode())
    time.sleep(0.1)
    client.send(str(file_size).encode())
    time.sleep(0.1)
    md5sum = hashlib.md5(data).hexdigest().encode()
    print(md5sum)
    client.send(md5sum)
    time.sleep(0.1)
    desc = ent_descp.get()
    if desc == '':
        client.send('<NOT PROVIDED>'.encode())
    else:
        client.send(desc.encode())
    time.sleep(0.1)
    # recv = False
    # while not recv:
    #     confirm = client.recv(1024).decode().lower()
    #     if confirm == 'y' or confirm == 'n': recv = True
    #     else: continue
    
    
        # file.close()
        # client.close()
        # showerror('Socket Transmitter Tool', 'ConnectionRefusedError: REQUSET REFUSED BY RECEIVING SIDE!')
    
    
    encoded_file = base64.b64encode(data)
    client.sendall(encoded_file)
    # print(encoded_file)
    
    # time.sleep(0.1)
    client.send(b'!End:...')
    time.sleep(0.1)
    file.close()

    if client.recv(1024).decode() == 'ERROR':
        showerror('Socket Transmitter Tool', 'ConnectionError: Operation failed, try again')
    else:
        showinfo('Socket Transmitter Tool', 'Operation succeed!')
    
    client.close()


# btn_check = Button(text='check')
btn_send = Button(text='send download request', command=SendFileCommand)
btn_browse = Button(text='Browse', command=browseCommand)

# packing
lab_targetIP.grid(row=0, column=0, padx=5, pady=5)
ent_IP.grid(row=0, column=1, padx=5, pady=5)

lab_port.grid(row=1, column=0, padx=5, pady=5)
ent_port.grid(row=1, column=1, padx=5, pady=5)

lab_filepath.grid(row=2, column=0, padx=5, pady=5)
ent_filepath.grid(row=2, column=1, padx=5, pady=5)
btn_browse.grid(row=2, column=2, padx=5, pady=5)

lab_targetfilename.grid(row=3, column=0, padx=5, pady=5)
ent_filename.grid(row=3, column=1, padx=5, pady=5)
lab_description.grid(row=4, column=0, padx=5, pady=5)
ent_descp.grid(row=4, column=1, padx=5, pady=5)
# chk_empty.grid(row=4, column=2, padx=5, pady=5)
btn_send.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

window.mainloop()