from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class department:
    def __init__(self, root):
        self.root = root
        self.root.title("Department")
        self.root.geometry('600x600')
        self.root.configure(bg='lightblue')

        self.departmentidLabel = Label(root, text="Department:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentidLabel.grid(row=0, column=0)
        self.departmentidVar = StringVar()
        self.departmentidEntry = Entry(root, textvariable=self.departmentidVar)
        self.departmentidEntry.grid(row=0, column=1, padx=10, pady=10)

        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=1, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=2, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('id', 'name'), show='headings')
        for col in ('id', 'name'):
            self.tree.heading(col, text=col)
        self.tree.grid(row=6, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=8, column=0, columnspan=2, pady=10)
        self.load_data()

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
        dept = self.departmentidVar.get()
        print(dept)
        if dept:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV8"
                )
                cursor = db.cursor()
                sql = "INSERT INTO department (name) VALUES ('" + dept + "')"
                cursor.execute(sql)
                db.commit()
                messagebox.showinfo("Success", "Record inserted successfully.")
                db.close()
                self.load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def fetch_data(self):
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV8"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM department")
        rows = cursor.fetchall()
        db.close()
        return rows

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
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBaseV8"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM department WHERE ID = %s", (record_id,))
        db.commit()
        db.close()
        self.load_data()

if __name__ == "__main__":
    root = Tk()
    app = level(root)
    root.mainloop()
