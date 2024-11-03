from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class Instructor:
    def __init__(self, master):
        self.master = master
        self.master.title('Instructor')
        self.master.geometry('600x500')
        self.master.configure(bg='lightblue')
        
        self.setup_widgets()
        self.load_data()

    def setup_widgets(self):
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        # Name Entry
        Label(self.master, text="Name", **label_style).grid(row=0, column=0, padx=10, pady=10)
        self.name = StringVar()
        Entry(self.master, textvariable=self.name, **entry_style).grid(row=0, column=1, padx=10, pady=10)

        # Position Radiobuttons
        self.position = StringVar()
        self.position.set("Dr")
        Radiobutton(self.master, text='Dr', variable=self.position, value="Dr", bg='lightblue', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10)
        Radiobutton(self.master, text='TA', variable=self.position, value="TA", bg='lightblue', font=('Arial', 12)).grid(row=1, column=1, padx=10, pady=10)

        # Submit Button
        Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db).grid(row=3, column=0, columnspan=2, pady=20)

        # Load Data Button
        Button(self.master, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data).grid(row=4, column=0, columnspan=2, pady=10)

        # Treeview for Displaying Data
        self.tree = ttk.Treeview(self.master, columns=('Id', 'Name', 'Role'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.grid(row=5, column=0, columnspan=2, pady=20)

        # Delete Button
        Button(self.master, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record).grid(row=6, column=0, columnspan=2, pady=10)

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
        except Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def insert_to_db(self):
        name = self.name.get()
        position = self.position.get()

        if name and position:
            db = self.connect_db()
            if db:
                try:
                    cursor = db.cursor()
                    sql = "INSERT INTO instructor (Name, Role) VALUES (%s, %s)"
                    cursor.execute(sql, (name, position))
                    db.commit()
                    messagebox.showinfo("Registration Success", "User registered successfully.")
                    self.load_data()
                except Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                finally:
                    db.close()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def fetch_data(self):
        db = self.connect_db()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute("SELECT id, name, role FROM instructor")
                return cursor.fetchall()
            except Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
                return []
            finally:
                db.close()
        return []

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_data()
        for row in rows:
            self.tree.insert("", END, values=row)

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a record to delete")
            return

        record_id = self.tree.item(selected_item[0], 'values')[0]
        db = self.connect_db()
        if db:
            try:
                cursor = db.cursor()
                cursor.execute("DELETE FROM instructor WHERE id = %s", (record_id,))
                db.commit()
                self.tree.delete(selected_item[0])
                messagebox.showinfo("Success", "Record deleted successfully.")
            except Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                db.close()

if __name__ == "__main__":
    root = Tk()
    app = Instructor(root)
    root.mainloop()