from tkinter import *
from tkinter import messagebox

from gui.widgets.text_box import TextBox
from observers.gui_events import event_pressed_send_message, event_closed_chat_window

class ChatWindow():
    
    WIDTHPIXELS = 1000
    HEIGHTPIXELS = 500

    def __init__(self, master, chating_with):
        self.master = master
        self.root = Tk()
        self.root.geometry('%dx%d' % (self.WIDTHPIXELS, self.HEIGHTPIXELS))
        self.center()
        self.chating_with = chating_with
        self.root.title('Chat with %s' % chating_with)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.pending_message = False

        logTextFrame = Frame(self.root, bd=1, relief=SUNKEN)
        logTextFrame.pack(anchor=N, fill=BOTH, side=TOP)
        self.logText = TextBox(self.root)

        sendTextFrame = Frame(self.root, bd=1, relief=SUNKEN)
        sendTextFrame.pack(anchor=S, fill=BOTH, side=BOTTOM)
        
        sendTextBox = Frame(sendTextFrame, bd=1, relief=SUNKEN)
        sendTextBox.pack(expand=1, fill=BOTH, side=LEFT)
        self.msgText = TextBox(sendTextBox, NORMAL)

        sendButtonBox = Frame(sendTextFrame, bd=1, relief=SUNKEN)
        sendButtonBox.pack(side=RIGHT)
        sendTextButton = Button(sendButtonBox, text='Send', command=lambda: self.send_message())
        sendTextButton.pack()

    def send_message(self):
        if self.pending_message:
            messagebox.showwarning('Cannot send message', 'Message pendig to %s.' % self.chating_with, parent=self.root)
        else:
            self.pending_message = True
            self.master.update(event_pressed_send_message, msg=self.msgText.get_text(), to=self.chating_with)

    def msg_success(self):
        self.pending_message = False
        self.logText.log('You: %s' % self.msgText.get_text())
        self.logText.clean()

    def msg_received(self, msg):
        self.pending_message = False
        self.logText.log('%s: %s' % (self.chating_with, msg))

    def msg_fail(self):
        self.pending_message = False
        messagebox.showerror('Message was not sent', 'Fail to send message to %s' % self.chating_with, parent=self.root)

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def on_close(self):
        self.master.update(event_closed_chat_window, username=self.chating_with)
        self.root.destroy()

    def raises(self):
        self.root.withdraw()
        self.center()
        self.root.deiconify()
