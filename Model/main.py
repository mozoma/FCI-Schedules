from tkinter import *
from department import department
from level import Level
from instructor import Instructor
from subject import Subject
from load import Load
from Createtable import CreateTable
from location import LocationPageADD

class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Main Page')
        self.master.geometry('400x200')
        self.master.configure(bg='lightblue')
        
        button_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}

        self.department= Button(self.master, text="Department", **button_style, command=self.open_DepaetmentPage)
        self.department.grid(row=0, column=0, pady=10)
        
        self.level = Button(self.master, text="level", **button_style, command=self.open_level)
        self.level.grid(row=0, column=1, pady=10)

        self.instructor = Button(self.master, text="instructor", **button_style, command=self.open_Instructor)
        self.instructor.grid(row=1, column=0, pady=10)

        self.subject = Button(self.master, text="subject", **button_style, command=self.open_subject)
        self.subject.grid(row=1, column=1, pady=10)

        self.location = Button(self.master, text="location", **button_style, command=self.open_location)
        self.location.grid(row=2, column=0, pady=10)        

        self.load = Button(self.master, text="load", **button_style, command=self.open_load)
        self.load.grid(row=2, column=1, pady=10)

        self.Createtable = Button(self.master, text="Createtable", **button_style, command=self.open_Createtable)
        self.Createtable.grid(row=3, column=0, pady=10)

        self.Exit = Button(self.master, text="Exit", **button_style, command=self.close_window)
        self.Exit.grid(row=3, column=1, pady=10)
    
    def open_DepaetmentPage(self):
        self.new_window(department)

    def open_Instructor(self):
        self.new_window(Instructor)
        
    def open_location(self):
        self.new_window(LocationPageADD)
        
    def open_subject(self):
        self.new_window(Subject)

    def open_level(self):
        self.new_window(Level)

    def open_load(self):
        self.new_window(Load)

    def open_Createtable(self):
        self.new_window(CreateTable)    

    def new_window(self, _class):
        new = Toplevel(self.master)
        _class(new)
        
    def close_window(self):
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = MainPage(root)
    root.mainloop()