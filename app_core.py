from tkinter import Tk
from login import Login
from main_tab import MainWindow


class PasswordManager:
    __root = Tk()
    __thisWidth = 450
    __thisHeight = 240

    def __init__(self, **kwargs):
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass
        self.__root.title("Password Manager")
        self.bg_color = 'white'
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))
        self.frame1 = Login(self.run_main_frame, self.__root)

    def run_main_frame(self):
        self.frame2 = MainWindow(self.login_return, self.__root)

    def login_return(self):
        self.frame1 = Login(self.run_main_frame, self.__root)

    def run(self):
        # Run main application
        self.__root.mainloop()

    def __quitApplication(self):
        self.__root.destroy()
