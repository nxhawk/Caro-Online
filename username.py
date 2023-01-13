import tkinter as tk
import textstyles as style


class Connect(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.create_widgets()

    def create_widgets(self):
        self.spacer = tk.Label(self, height=8, width=26, anchor=tk.E)
        self.spacer.grid(row=0, column=0)

        self.lbl_ip = tk.Label(self, height=1, text="User name:",
                               width=15, justify="left", font="Helvetica 25 bold roman", anchor=tk.W)
        self.lbl_ip.grid(row=1, column=1, sticky=tk.E+tk.W,
                         padx=5, pady=0, columnspan=1)
        self.txt_ip = tk.Entry(
            self, width=36, font=style.entry_font, bg="#FFFFFF")
        self.txt_ip.grid(row=2, column=1, sticky=tk.E,
                         padx=5, pady=5, columnspan=1)

        self.btn_connect = tk.Button(self, text="Connect", width=10, height=1, font=style.btn_font,
                                     activebackground=style.btn_style['actbg'], bg=style.btn_style['bg'], fg=style.btn_style['fg'])
        self.btn_connect.grid(row=5, column=1, sticky=tk.S +
                              tk.N, padx=5, pady=5, columnspan=1)

    def get_info(self):
        return self.txt_ip.get()

    def clear_all(self):
        self.txt_ip.delete(0, tk.END)
