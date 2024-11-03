from tkinter import *
from tkinter import messagebox, ttk

class LevelView: 
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Level")
        self.root.geometry('500x500')
        self.root.configure(bg='lightblue')

        self.departmentidLabel = Label(root, text="Department:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentidLabel.grid(row=0, column=0)
        self.departmentidVar = StringVar()
        self.departmentidEntry = ttk.Combobox(root, textvariable=self.departmentidVar)
        self.departmentidEntry.grid(row=0, column=1, padx=10, pady=10)

        self.levelLabel = Label(root, text="Level:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.levelLabel.grid(row=1, column=0)
        self.levelVar = IntVar()
        self.levelEntry = ttk.Combobox(root, textvariable=self.levelVar, values=[1, 2, 3, 4])
        self.levelEntry.grid(row=1, column=1, padx=10, pady=10)

        self.sectionsLabel = Label(root, text="Number of Sections:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.sectionsLabel.grid(row=2, column=0)
        self.sectionsVar = IntVar()
        self.sectionsEntry = Entry(root, textvariable=self.sectionsVar)
        self.sectionsEntry.grid(row=2, column=1, padx=10, pady=10)

        self.submitButton = Button(root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.controller.submit_record)
        self.submitButton.grid(row=3, column=0, columnspan=2, pady=20)

        self.loadButton = Button(root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.controller.load_data)
        self.loadButton.grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(root, columns=('id', 'department', 'level', 'sections'), show='headings')
        for col in ('id', 'department', 'level', 'sections'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=8, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.controller.delete_record)
        self.deleteButton.grid(row=7, column=0, columnspan=2, pady=10)

    def populate_departments(self, departments):
        self.departmentidEntry['values'] = [name for _, name in departments]

    def populate_tree(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", END, values=row)

    def get_selected_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0], 'values')
        return None

from tkinter import Tk
from controller import LevelController  # Ensure you import LevelController from the correct file

if __name__ == "__main__":
    root = Tk()
    app = LevelController(root)
    root.mainloop()
 
