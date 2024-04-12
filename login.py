from tkinter import Frame, Label, Entry, Button, END
from shared_values import Shared


class Login(Frame):
    font = 'Arial 12'

    def __init__(self, fun, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fun = fun
        self.pack(fill='both', expand=True, anchor="center")
        self.labels()
        self.entries()
        self.buttons()

    def labels(self):
        self.space_label = Label(self, text="     ", font=self.font)
        self.space_label1 = Label(self, text="     ", font=self.font)
        self.space_label4 = Label(self, text="         ", font=self.font)
        self.space_label5 = Label(self, text="         ", font=self.font)

        self.login_label = Label(self, text="Login ", font=self.font,  anchor="e")
        self.password_label = Label(self, text="Password ", font=self.font,  anchor="e")

        self.space_label.grid(row=1, column=1, sticky='ew')
        self.space_label1.grid(row=2, column=1, sticky='ew')
        self.space_label4.grid(row=3, column=1, sticky='ew')
        self.space_label5.grid(row=4, column=1, sticky='ew')

        self.login_label.grid(row=3, column=2, sticky='ew')
        self.password_label.grid(row=4, column=2, sticky='ew')

    def entries(self):

        self.login_entry = Entry(self,  font=self.font, width=20)
        self.password_entry = Entry(self, font=self.font, width=20)
        self.login_entry.grid(row=3, column=3, sticky='ew')
        self.password_entry.grid(row=4, column=3, sticky='ew')

    def buttons(self):
        self.log_in_button = Button(self, text="Log in", command=self.connect, width=11)
        self.clear_button = Button(self, text="Clear", command=self.clear, width=11)
        self.log_in_button.grid(row=5, column=3, sticky='e')
        self.clear_button.grid(row=5, column=3, sticky='w')

    def clear(self):
        self.login_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def connect(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        try:
            self.warning = Label(self, text="", font=self.font, anchor="e")
            self.warning.grid(row=6, column=3, sticky='ew')
            Shared.pg.set_connection(
                                            user=login,
                                            password=password,
                                            host=Shared.config.host,
                                            port=Shared.config.port,
                                            database=Shared.config.database
                                        )
        except:
            self.warning = Label(self, text="Wrong Login or Password!", font=self.font, anchor="e")
            self.warning.grid(row=6, column=3, sticky='ew')
        else:
            self.clear()
            self.destroy()
            self.fun()
