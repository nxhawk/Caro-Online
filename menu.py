import tkinter as tk
from username import Connect


class Login(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.usr = None

        self.geometry('800x400')
        self.title('Username')
        self.resizable(False, False)
        self.grid()

        # Header
        self.head = tk.Frame(self, bg='#7ed6df')
        self.head.pack(side='top', fill='both', expand=1)
        self.head.grid_rowconfigure(0, weight=1)
        self.head.grid_columnconfigure(0, weight=1)

        # Body
        self.body = tk.Frame(self)
        self.body.pack(side="top", fill="both", expand=True)
        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.frame = Connect(parent=self.body)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()
        self.bind_action()

    def bind_action(self):
        self.bind("<Destroy>", self.quit_prog)
        self.frame.btn_connect['command'] = self.connect

    def connect(self):
        username = self.frame.get_info()
        username = username.strip(' ')
        self.usr = username
        self.destroy()

    def quit_prog(self, event):
        try:
            if str(event.widget) == '.':
                pass
        except:
            pass

    def create_header(self):
        '''Init header element'''
        self.lbl_app = tk.Label(
            self.head, text='Login with Username', height=1, font="Helvetica 15 bold roman", bg="#f9cdad", fg="#ec2049")
        self.lbl_app.grid(row=0, column=0, sticky=tk.W, padx=30, pady=10,
                          ipadx=10, ipady=10, columnspan=2, rowspan=2)

    def run(self):
        self.mainloop()
        return self.usr
