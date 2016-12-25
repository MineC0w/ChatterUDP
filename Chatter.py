'''

A UDP chat application.

'''

import Tkinter
import socket
import threading, time
import Client
import tkMessageBox
from PIL import Image, ImageTk

__author__ = 'Yair'

#Create UDP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

chatters = {} # Active chatters dictionary
mainWidgets = {} # Widgets of main form, actually not necessary and might be bad programming
newChatWidgets = {} # This one is actually useless
recMessage = True # Receive message thread
socketTimeout = 0.5 # Socket timeout set to 0.5 seconds




ip = "10.0.0.6"
port = 8820


def send(data):
    global mainWidgets, soc, chatters
    if "chatList" not in mainWidgets:
        print "List not found."
        return
    else:
        selection = mainWidgets["chatList"].get(Tkinter.ACTIVE)
        if selection not in chatters:
            print "Error: User not found"
        else:
            soc.sendto(str(data), chatters[selection].getSendAdd())

def newChat():
    global mainWidgets, soc
    if "chatList" not in mainWidgets:
        print "List not found."
        return
    else:
        newChatForm()
def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    mainWidgets["chatBox"].delete('1.0', Tkinter.END)
    mainWidgets["chatBox"].insert(Tkinter.END, chatters[value].getChat())

def newChatForm():
    LoginForm = Tkinter.Tk() # Login Screen
    LoginForm.wm_title("New Chat")
    IPLabel = Tkinter.Label(LoginForm, text = "IP (or Domain)")
    IPLabel.grid(row = 0, column = 0)

    PortLabel = Tkinter.Label(LoginForm, text = "Port")
    PortLabel.grid(row = 1, column = 0)

    IPEntry = Tkinter.Entry(LoginForm, text = "IP")
    IPEntry.grid(row = 0, column = 1)

    PortEntry = Tkinter.Entry(LoginForm, text = "Port")
    PortEntry.grid(row = 1, column = 1)

    ConnectButton = Tkinter.Button(LoginForm, text = "Connect", command = lambda: addchat(IPEntry.get(), PortEntry.get(), LoginForm))
    ConnectButton.grid(row = 2, column = 0, columnspan = 2, sticky=Tkinter.E+Tkinter.W)

    LoginForm.mainloop()

def addchat(ip, port, form):
    global mainWidgets, chatters
    mainWidgets["chatList"].insert(0, ip)
    newClient = Client.Client(ip, int(port))
    chatters[ip] = newClient
    form.destroy()

def receive():
    global soc, widgets
    while recMessage:
        try:
            (data, sender) = soc.recvfrom(1024)
            if sender[0] not in mainWidgets["chatList"].get(0,Tkinter.END):
                newClient = Client.Client(sender[0], sender[1])
                mainWidgets["chatList"].insert(0, sender[0])
                chatters[sender[0]] = newClient
            msg =  "%s (%s): %s\n" % (sender[0], str(sender[1]), data)
            mainWidgets["chatBox"].configure(state="normal")
            mainWidgets["chatBox"].insert(Tkinter.END, msg)
            mainWidgets["chatBox"].configure(state="disabled")
            chatters[sender[0]].addChat(msg)
            print "Received %s from %s" % (str(data), str(sender))
        except socket.timeout:
            #print "Nothing received."
            pass




def kill(window, sock):
    global recMessage
    # Close the window
    window.destroy()
    # Disable message receiving so thread could exit safely
    recMessage = False
    # Make sure socket doesn't close too soon
    time.sleep(socketTimeout)
    sock.close()

def main():
    global mainWidgets, soc
    window = Tkinter.Tk()
    window.wm_title("Chat! %s" % (str(ip)))
    mainWidgets["chatList"] = Tkinter.Listbox(window)

    mainWidgets["chatList"].bind("<<ListboxSelect>>", onselect)
    mainWidgets["chatList"].grid(row = 0, column = 0,sticky=Tkinter.N+Tkinter.S)

    mainWidgets["chatBox"] = Tkinter.Text(window)
    mainWidgets["chatBox"].grid(row = 0, column = 1)
    tstEmoji = Image.open("emojis/upside_down_smile.png")

    tstEmoji2 = ImageTk.PhotoImage(tstEmoji.resize((16,16), Image.ANTIALIAS))

    mainWidgets["chatBox"].image_create(Tkinter.END, image=tstEmoji2)
    mainWidgets["chatBox"].configure(state="disabled")
    mainWidgets["chatBox"].bind("<1>", lambda event:mainWidgets["chatBox"].focus_set())
    mainWidgets["chatInput"] = Tkinter.Entry(window)
    mainWidgets["chatInput"].grid(row = 1, rowspan = 2,column = 1, sticky = Tkinter.W+Tkinter.E+Tkinter.S+Tkinter.N)
    mainWidgets["sendInput"] = Tkinter.Button(window, text = "Send", command = lambda: send(mainWidgets["chatInput"].get()))
    mainWidgets["sendInput"].grid(row = 1, column = 0, sticky = Tkinter.W+Tkinter.E)

    mainWidgets["newChatBtn"] = Tkinter.Button(window, text = "New Chat", command = newChat)
    mainWidgets["newChatBtn"].grid(row = 2, column = 0, sticky = Tkinter.W+Tkinter.E)

    soc.bind((ip, port))
    soc.settimeout(socketTimeout)


    window.protocol("WM_DELETE_WINDOW", lambda: kill(window, soc))
    receiveThread = threading.Thread(target = receive, args = ())
    receiveThread.start()

    window.mainloop()

if __name__ == "__main__":
    main()

