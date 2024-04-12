from tkinter import Frame, Label, Entry, Button, END, messagebox
from shared_values import Shared


class MainWindow(Frame):
    font = 'Arial 12'

    def __init__(self, fun,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill='both', expand=True, anchor="center")
        self.fun = fun
        self.labels()
        self.entries()
        self.buttons()

    def labels(self):
        self.name_label = Label(self, text='Name: ', font=self.font, anchor='e')
        self.empty_line = Label(self, text='               ', font=self.font)
        self.login_label = Label(self,  text='Login: ', font=self.font, anchor='e')
        self.password_label = Label(self,  text='Password: ', font=self.font, anchor='e')
        self.email_label = Label(self, text='Email: ', font=self.font, anchor='e')
        self.PIN_label = Label(self,  text='PIN: ', font=self.font, anchor='e')
        self.phone_label = Label(self,  text='Phone Number: ', font=self.font, anchor='e')
        self.commentary_label = Label(self, text='Commentary: ', font=self.font, anchor='e')

        self.name_label.grid(row=1, column=1, sticky='ew')
        self.empty_line.grid(row=2, column=1, sticky='ew')
        self.login_label.grid(row=3, column=1, sticky='ew')
        self.password_label.grid(row=4, column=1, sticky='ew')
        self.email_label.grid(row=5, column=1, sticky='ew')
        self.PIN_label.grid(row=6, column=1, sticky='ew')
        self.phone_label.grid(row=7, column=1, sticky='ew')
        self.commentary_label.grid(row=8, column=1, sticky='ew')

    def entries(self):
        self.name_entry = Entry(self, font=self.font, width=20)
        self.login_entry = Entry(self, font=self.font, width=20)
        self.password_entry = Entry(self, font=self.font, width=20)
        self.email_entry = Entry(self, font=self.font, width=20)
        self.PIN_entry = Entry(self, font=self.font, width=20)
        self.phone_entry = Entry(self, font=self.font, width=20)
        self.commentary_entry = Entry(self, font=self.font, width=20)

        self.name_entry.grid(row=1, column=2, sticky='ew')
        self.login_entry.grid(row=3, column=2, sticky='ew')
        self.password_entry.grid(row=4, column=2, sticky='ew')
        self.email_entry.grid(row=5, column=2, sticky='ew')
        self.PIN_entry.grid(row=6, column=2, sticky='ew')
        self.phone_entry.grid(row=7, column=2, sticky='ew')
        self.commentary_entry.grid(row=8, column=2, sticky='ew')

    def buttons(self):
        self.get_record = Button(self, text="Display", command=self.display, width=11)
        self.clear_button = Button(self, text="Clear", command=self.clear, width=11)
        self.modify_button = Button(self, text="Modify", command=self.modify, width=11)
        self.insert_button = Button(self, text="Insert", command=self.insert, width=11)
        self.delete_button = Button(self, text="Delete", command=self.delete, width=11)
        self.logout_button = Button(self, text="Log out", command=self.logout, width=11)

        self.get_record.grid(row=1, column=3, sticky='e')
        self.clear_button.grid(row=2, column=3, sticky='w')
        self.modify_button.grid(row=3, column=3, sticky='w')
        self.insert_button.grid(row=4, column=3, sticky='w')
        self.delete_button.grid(row=5, column=3, sticky='w')
        self.logout_button.grid(row=7, column=3, sticky='w')

    def display(self):
        entry = self.name_entry.get()
        login = self.login_entry.get()

        cols = Shared.pg.get_record_subset(table_name=Shared.config.table, col_names=['Name', 'Login'])

        if login == "":
            cols = cols.loc[cols['Name'] == entry]
        else:
            cols = cols.loc[(cols['Name'] == entry) & (cols['Login'] == login)]

        if len(cols) > 1 and login == "":

            logins = cols['Login'].tolist()
            self.communicate = Label(self,  text=f"Select login from the list: {[login for login in logins]}",
                                     font=self.font, anchor='e')

        elif len(cols) == 1:
            self.communicate = Label(self,  text=f"", font=self.font, anchor='e')
            self.communicate.grid(row=9, column=2, sticky='ew')
            cols = cols.reset_index(drop=True)

            df = Shared.pg.get_record_df_and_condition(table_name=Shared.config.table,
                                                       where={'Name': entry, "Login": cols.at[0, 'Login']})
            df = df.fillna(value="")

            self.clear()

            self.name_entry.insert(0, str(df['Name'].values[0]))
            self.login_entry.insert(0, str(df['Login'].values[0]))
            self.password_entry.insert(0, str(df['Password'].values[0]))
            self.email_entry.insert(0, str(df['Email'].values[0]))
            self.PIN_entry.insert(0, str(df['PIN'].values[0]))
            self.phone_entry.insert(0, str(df['Phone Number'].values[0]))
            self.commentary_entry.insert(0, str(df['Comment'].values[0]))
        else:
            self.communicate = Label(self,  text=f"No a such Name stored!", font=self.font, anchor='e')

        self.communicate.grid(row=9, column=2, sticky='ew')

    def clear(self):
        self.communicate = Label(self, text=f"", font=self.font, anchor='e')
        self.communicate.grid(row=9, column=2, sticky='ew')
        self.name_entry.delete(0, END)
        self.login_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.PIN_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.commentary_entry.delete(0, END)

    def modify(self):
        name = self.name_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        pin = self.PIN_entry.get()
        phone = self.phone_entry.get()
        comment = self.commentary_entry.get()

        cols = Shared.pg.get_record_subset(table_name=Shared.config.table, col_names=['Name', 'Login'])

        if login == "":
            cols = cols.loc[cols['Name'] == name]
        else:
            cols = cols.loc[(cols['Name'] == name) & (cols['Login'] == login)]
        cols = cols.reset_index(drop=True)

        if len(cols) > 1 and login == "":
            logins = cols['Login'].tolist()
            self.communicate = Label(self,  text=f"Select login from the list: {[login for login in logins]}",
                                     font=self.font, anchor='e')
        elif len(cols) == 1:
            if login == "":
                update_on = {'Name': name, 'Login': cols.at[0, 'Login']}
            else:
                update_on = {'Name': name, 'Login': login}
            to_update = {'Name': name,
                         'Login': login,
                         'Password': password,
                         'Email': email,
                         'PIN': pin,
                         'Phone Number': phone,
                         'Comment': comment}
            to_update = {key: val for key, val in to_update.items() if val != ""}
            try:
                Shared.pg.update_record_condition_and(table_name=Shared.config.table,
                                                      to_update=to_update,
                                                      update_on_fields=update_on)
            except:
                self.communicate = Label(self, text=f"Modification Error!", font=self.font, anchor='e')
            else:
                self.communicate = Label(self,  text=f"Record modified!", font=self.font, anchor='e')
        else:
            self.communicate = Label(self,  text=f"No a such Name stored!", font=self.font, anchor='e')

        self.communicate.grid(row=9, column=2, sticky='ew')

    def insert(self):
        name = self.name_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        pin = self.PIN_entry.get()
        phone = self.phone_entry.get()
        comment = self.commentary_entry.get()

        cols = Shared.pg.get_record_subset(table_name=Shared.config.table, col_names=['Name', 'Login'])

        if name == "" or login == "" or password == "":
            self.communicate = Label(self,  text=f"Fields: Name, Login and Passwords are mandatory!",
                                            font=self.font,
                                            anchor='e')

        elif not cols.loc[(cols['Name'] == name) & (cols['Login'] == login)].empty:
            self.communicate = Label(self, text=f"Record with provided Name and Loging already exists!",
                                           font=self.font,
                                           anchor='e')
        else:
            to_insert = {'Name': name,
                         'Login': login,
                         'Password': password,
                         'Email': email,
                         'PIN': pin,
                         'Phone Number': phone,
                         'Comment': comment}
            to_insert = {key: val if val != "" else 'NULL' for key, val in to_insert.items()}
            try:
                Shared.pg.insert_record(table_name=Shared.config.table, to_insert=to_insert)
            except:
                self.communicate = Label(self, text=f"Insertion Error!", font=self.font, anchor='e')
            else:
                self.communicate = Label(self, text=f"Record inserted!", font=self.font, anchor='e')

        self.communicate.grid(row=9, column=2, sticky='ew')

    def delete(self):
        result = messagebox.askyesno("WARNING!", "Do you want to delete selected record?")
        if result:
            name = self.name_entry.get()
            login = self.login_entry.get()

            cols = Shared.pg.get_record_subset(table_name=Shared.config.table, col_names=['Name', 'Login'])
            if login == "":
                cols = cols.loc[cols['Name'] == name]
            else:
                cols = cols.loc[(cols['Name'] == name) & (cols['Login'] == login)]

            cols = cols.reset_index(drop=True)

            if len(cols) > 1 and login == "":
                logins = cols['Login'].tolist()
                self.communicate = Label(self,  text=f"Select login from the list: {[login for login in logins]}",
                                         font=self.font, anchor='e')
            elif len(cols) == 1:
                if login == "":
                    to_del = {'Name': name, 'Login': cols.at[0, 'Login']}
                else:
                    to_del = {'Name': name, 'Login': login}

                try:
                    Shared.pg.delete_record_condition_and(table_name=Shared.config.table, field_identifier=to_del)
                except:
                    self.communicate = Label(self, text=f"Deletion Error!", font=self.font, anchor='e')
                else:
                    self.communicate = Label(self, text=f"Record deleted!", font=self.font, anchor='e')
            else:
                self.communicate = Label(self,  text=f"No a such Name stored!", font=self.font, anchor='e')

            self.communicate.grid(row=9, column=2, sticky='ew')
            self.clear()

    def logout(self):
        self.clear()
        Shared.pg.terminate_connection()
        self.destroy()
        self.fun()
