import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import socket


### FIXED VARIABLES
FIREBASE_URL = 'https://lab12-72730-default-rtdb.firebaseio.com/'
JSON_FILE = './/../lab-deliverables//lab12.json'

CRED = credentials.Certificate(JSON_FILE)
firebase_admin.initialize_app(CRED, {'databaseURL': FIREBASE_URL})
REF = firebase_admin.db.reference('/')


### GUI-RELATED FUNCTIONS
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
    
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        #
        self.nameLbl = tk.Label(self.groupCon, text='Name:', padx=10)
        self.nameLbl.pack(side="left")
        #
        self.name = tk.Entry(self.groupCon, width=20)
        self.name.insert(tk.END, 'John Smith')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.name.bind('<Return>', connectHandler)
        self.name.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")

        
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text = 'send',
            command = sendButtonClick)
        self.sendButton.pack(side="left")
        
        
        # set the focus on the IP and Port text field
        self.name.focus_set()


def sendButtonClick():
    # forward to the sendMessage method
    sendMessage(g_app)

# the connectHandler toggles the status between connected/disconnected
def connectHandler(master):
    tryToConnect()

# a utility method to print to the message field        
def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

# if attempt to close the window, it is handled here
def on_closing():
    if g_bConnected:
        if tkmsgbox.askokcancel("Quit",
            "You are still connected. If you quit you will be"
            + " disconnected."):
            myQuit()
    else:
        myQuit()

# when quitting, do it the nice way    
def myQuit():
    g_root.destroy()

def streamHandler(incomingData):
    """
        handles incoming data from the server
    """
    g_root.after(g_pollFreq, streamHandler)

    if incomingData.event_type == 'put':
        if incomingData.path == '/':
            # this is the very first reading just after subscription:
            # we get all messages or None (if no messages exists)
            if incomingData.data != None:
                for key in incomingData.data:
                    message = incomingData.data[key]
                    handleMessage(message)
        else:
            # not the first reading
            # someone wrote a new message that we just got
            message = incomingData.data
            handleMessage(message)


def handleMessage(message):
    """
        prints message to the gui
    """
    printToMessages(message['name'] + ': ' + message['message'])

    
# attempt to connect to server    
def tryToConnect():
    # subscribe to the messages once start up
    messages_stream = REF.child('messages').listen(streamHandler)


# attempt to send the message (in the text field g_app.textIn) to the server
def sendMessage(master):
    # a call to g_app.textIn.get() delivers the text field's content
    message_text = g_app.textIn.get()
    name = g_app.name.get()
    new_message = {'name': name, 'message': message_text}
    REF.child('messages').push(new_message)


g_bConnected = False
g_pollFreq = 200

# launch the gui
g_root = tk.Tk()
g_app = Application(master=g_root)


# schedule the next call to pollMessages
g_root.after(g_pollFreq, streamHandler)

# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()
