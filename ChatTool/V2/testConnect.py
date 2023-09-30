import tkinter as tk
import socket

from tkinter.messagebox import *

window = tk.Tk()
window.title('Connection Tester')
window.resizable(False, False)
window.rowconfigure(0, minsize=0, weight=1)
window.columnconfigure(1, minsize=0, weight=1)

frm_data = tk.Frame()

lab_ip = tk.Label(frm_data, text='Target IP')
lab_port = tk.Label(frm_data, text='Scanned port')

ent_ip = tk.Entry(frm_data, width=45)
ent_port = tk.Entry(frm_data, width=45)



def test():
    try:
        target = ent_ip.get()
        port = int(ent_port.get())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
            
        # returns an error indicator
        result = s.connect_ex((target,port))
        if result == 0:
            showinfo('Scanner', f'Port {port} is opened')
        else:
            showinfo('Scanner', f'Port {port} is closed')
        s.close()
    
    except socket.gaierror:
        showerror('Scanner', 'Host name couldn\'t be resolved')
    
    except socket.error:
            showerror("Scanner", "Server not responding !!!!")

    except ValueError:
        showerror("Scanner", f"Wrong IP/PORT value \"{ent_port.get()}\"")

btn_test = tk.Button(text='Test Connection', command=test)

frm_data.grid(row=0, column=0, padx=5, pady=5)

lab_ip.grid(row=0, column=0, padx=5, pady=5)
ent_ip.grid(row=0, column=1, padx=5, pady=5)

lab_port.grid(row=1, column=0, padx=5, pady=5)
ent_port.grid(row=1, column=1, padx=5, pady=5)

btn_test.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

window.mainloop()