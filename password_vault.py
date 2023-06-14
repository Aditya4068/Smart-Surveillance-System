import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog
from tkinter import StringVar
from tkinter import ttk
from functools import partial
import uuid
import pyperclip
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from random import choice, randint, shuffle
#from main import main_window
from maingui import main_gui
#import tkinter.messagebox


backend = default_backend()
salt = b'2444'


kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=backend
)

encryptionKey = 0

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(message: bytes, token: bytes) -> bytes:
    return Fernet(token).decrypt(message)


#database code
with sqlite3.connect('password_vault.db') as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
recoveryKey TEXT NOT NULL);
""")

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS vault(
#id INTEGER PRIMARY KEY,
#website TEXT NOT NULL,
#username TEXT NOT NULL,
#password TEXT NOT NULL);
#""")

#Create PopUp
def popUp(text):
    #answer = simpledialog.askstring("Enter Details", text)
    top= Toplevel(window)
    #top.geometry("750x250")
    top.title("Enter Details")
    lx = Label(top, text= text, padx=20, pady=10)#.place(x=150,y=80)
    lx.pack()
    var = StringVar()
    answer = ttk.Entry(top, width=20, textvariable=var)
    
    answer.pack(padx=10, pady=10)
    answer.focus()
    def on_ok():
        top.destroy()

    btn = ttk.Button(top, text="Submit", command=on_ok)
    btn.pack(pady=10)
    
    top.wait_window()
    return var.get()


def popUp2(text):
    #tkinter.messagebox.showinfo("Generated Password",  text)
    top= Toplevel(window)
    #top.geometry("750x250")
    top.title("Generated Password")
    lx = Label(top, text= text, padx=20, pady=10)#.place(x=150,y=80)
    lx.pack()
    lx2 = Label(top, text= "Copied to clipboard!", padx=20, pady=10)#.place(x=150,y=80)
    lx2.pack()

#Initiate window
window = Tk()
window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "light")
window.update()

window.title("Passbox")

logo_img = PhotoImage(file="passboxlogo.png")

def hashPassword(input):
    hash1 = hashlib.sha256(input)
    hash1 = hash1.hexdigest()

    return hash1

def firstTimeScreen():
    for widget in window.winfo_children():
        widget.destroy()
    window.minsize(250,125)
    #window.geometry('250x125')
    lbl = ttk.Label(window, text="Choose a Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = ttk.Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = ttk.Label(window, text="Re-enter password")
    lbl1.config(anchor=CENTER)
    lbl1.pack()

    txt1 = ttk.Entry(window, width=20, show="*")
    txt1.pack()

    def savePassword():
        if txt.get() == txt1.get():
            sql = "DELETE FROM masterpassword WHERE id = 1"

            cursor.execute(sql)

            hashedPassword = hashPassword(txt.get().encode('utf-8'))
            key = str(uuid.uuid4().hex)
            recoveryKey = hashPassword(key.encode('utf-8'))

            global encryptionKey
            encryptionKey = base64.urlsafe_b64encode(kdf.derive(txt.get().encode()))
            
            insert_password = """INSERT INTO masterpassword(password, recoveryKey)
            VALUES(?, ?) """
            cursor.execute(insert_password, ((hashedPassword), (recoveryKey)))
            db.commit()

            recoveryScreen(key)
        else:
            lbl.config(text="Passwords dont match")
    
    def generate_password():
        
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
        password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        password = "".join(password_list)
        
        pyperclip.copy(password)
        popUp2(password)

    btn = ttk.Button(window, text="Save", command=savePassword)
    btn.pack(pady=5)

    btn = ttk.Button(window, text="Generate", command=generate_password)
    btn.pack(pady=5)

def recoveryScreen(key):
    for widget in window.winfo_children():
        widget.destroy()
    window.minsize(250,125)
    #window.geometry('250x125')
    lbl = ttk.Label(window, text="Save this key to be able to recover account")
    lbl.config(anchor=CENTER)
    lbl.pack()

    lbl1 = ttk.Label(window, text=key)
    lbl1.config(anchor=CENTER)
    lbl1.pack()

    def copyKey():
        pyperclip.copy(lbl1.cget("text"))

    btn = ttk.Button(window, text="Copy Key", command=copyKey)
    btn.pack(pady=5)

    def done():
        vaultScreen()

    btn = ttk.Button(window, text="Done", command=done)
    btn.pack(pady=5)

def resetScreen():
    for widget in window.winfo_children():
        widget.destroy()
    window.minsize(250,125)
    #window.geometry('250x125')
    lbl = ttk.Label(window, text="Enter Recovery Key")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = ttk.Entry(window, width=20)
    txt.pack()
    txt.focus()

    lbl1 = ttk.Label(window)
    lbl1.config(anchor=CENTER)
    lbl1.pack()

    def getRecoveryKey():
        recoveryKeyCheck = hashPassword(str(txt.get()).encode('utf-8'))
        cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND recoveryKey = ?', [(recoveryKeyCheck)])
        return cursor.fetchall()

    def checkRecoveryKey():
        checked = getRecoveryKey()

        if checked:
            firstTimeScreen()
        else:
            txt.delete(0, 'end')
            lbl1.config(text='Wrong Key')

    btn = ttk.Button(window, text="Check Key", command=checkRecoveryKey)
    btn.pack(pady=5)

def loginScreen():
    for widget in window.winfo_children():
        widget.destroy()

    #window.geometry('250x155')
    frame= ttk.Frame(window)
    frame.pack(fill= BOTH, expand= True, padx= 20, pady=20)

    #canvas = Canvas(frame, width=302, height=82)    
    #canvas.create_image(151, 41, image=logo_img)
    #canvas.pack()

    lbl = ttk.Label(frame, text="Enter Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = ttk.Entry(frame, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = ttk.Label(frame)
    lbl1.config(anchor=CENTER)
    lbl1.pack(side=TOP)

    def getMasterPassword():
        checkHashedPassword = hashPassword(txt.get().encode('utf-8'))
        global encryptionKey
        encryptionKey = base64.urlsafe_b64encode(kdf.derive(txt.get().encode()))
        cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND password = ?', [(checkHashedPassword)])
        return cursor.fetchall()

    def checkPassword():
        password = getMasterPassword()

        if password:
            vaultScreen()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Password")
    
    def resetPassword():
        resetScreen()

    btn = ttk.Button(frame, text="Submit", command=checkPassword)
    btn.pack(pady=5)

    btn = ttk.Button(frame, text="Reset Password", command=resetPassword)
    btn.pack(pady=5)


def vaultScreen():
    for widget in window.winfo_children():
        widget.destroy()
    window.destroy()
    main_gui()
    
    

cursor.execute('SELECT * FROM masterpassword')
if (cursor.fetchall()):
    loginScreen()
else:
    firstTimeScreen()
window.mainloop()


#5a0b741d816644198a0bd02a9518bcce

