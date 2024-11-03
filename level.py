from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Level:
    def __init__(self, root):
        self.root = root
        self.root.title("Level")
        self.root.geometry('500x500')
        self.root.configure(bg='lightblue')

        self.departments = self.fetch_departments()
        self.department_dict = {name: dept_id for dept_id, name in self.departments}

        self.departmentidLabel = Label(root, text="Department:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentidLabel.grid(row=0, column=0)
        self.departmentidVar = StringVar()
        self.departmentidEntry = ttk.Combobox(root, textvariable=self.departmentidVar)
        self.departmentidEntry['values'] = [name for name in self.department_dict.keys()]
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

        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=3, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('id', 'department', 'level', 'sections'), show='headings')
        for col in ('id', 'department', 'level', 'sections'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=8, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=7, column=0, columnspan=2, pady=10)

    def fetch_departments(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT ID, Name FROM department")
            rows = cursor.fetchall()
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def insert_to_db(self):
        department_name = self.departmentidVar.get()
        if department_name:
            dept_id = self.department_dict[department_name]
        else:
            dept_id = None

        levelNo = self.levelVar.get()
        No_sections = self.sectionsVar.get()

        if dept_id and levelNo and No_sections:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV8"
                )
                cursor = db.cursor()
                sql = "INSERT INTO level (Dept_ID, levelNo, No_sections) VALUES (%s, %s, %s)"
                cursor.execute(sql, (dept_id, levelNo, No_sections))
                db.commit()
                messagebox.showinfo("Success", "Record inserted successfully.")
                db.close()
                self.load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def fetch_data(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            query = """
            SELECT level.ID, department.Name, level.levelNo, level.No_sections
            FROM level
            JOIN department ON level.Dept_ID = department.ID
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_data()
        for row in rows:
            self.tree.insert("", END, values=row)

    def delete_record(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        record_id = values[0]
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("DELETE FROM level WHERE id = %s", (record_id,))
            db.commit()
            db.close()
            self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    root = Tk()
    app = Level(root)
    root.mainloop()
