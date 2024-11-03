from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
class LocationPageADD:
    def __init__(self, master):
        self.master = master
        self.master.title('Location Form')
        self.master.geometry('400x600')
        self.master.configure(bg='lightblue')
        
        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}
        
        # Location Type
        self.typeLabel = Label(self.master, text="Type", **label_style)
        self.typeLabel.grid(row=0, column=0, padx=10, pady=10)
        self.typeListbox = Listbox(self.master, selectmode=SINGLE, height=3, **entry_style)
        for item in ["Hall", "Room", "Lab"]:
            self.typeListbox.insert(END, item)
        self.typeListbox.grid(row=0, column=1, padx=10, pady=10)

        # Number
        self.HNumLabel = Label(self.master, text="Number", **label_style)
        self.HNumLabel.grid(row=1, column=0, padx=10, pady=10)
        self.HNum = StringVar()
        self.HNumEntry = Entry(self.master, textvariable=self.HNum, **entry_style)
        self.HNumEntry.grid(row=1, column=1, padx=10, pady=10)

        # Capacity
        self.capacityLabel = Label(self.master, text="Capacity", **label_style)
        self.capacityLabel.grid(row=2, column=0, padx=10, pady=10)
        self.capacity = StringVar()
        self.capacityEntry = Entry(self.master, textvariable=self.capacity, **entry_style)
        self.capacityEntry.grid(row=2, column=1, padx=10, pady=10)
        
        # Building Number
        self.buildingLabel = Label(self.master, text="Building Number", **label_style)
        self.buildingLabel.grid(row=3, column=0, padx=10, pady=10)
        self.buildingListbox = Listbox(self.master, selectmode=SINGLE, height=2, **entry_style)
        for item in ["A", "B"]:
            self.buildingListbox.insert(END, item)
        self.buildingListbox.grid(row=3, column=1, padx=10, pady=10)
        
        # Submit Button
        self.submitButton = Button(self.master, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=4, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.master, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=5, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.master, columns=('ID', 'capacity', 'name'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('capacity', text='Capacity')
        self.tree.heading('name', text='name')

        self.tree.grid(row=6, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.master, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=7, column=0, columnspan=2, pady=10)

        self.load_data()

    def insert_to_db(self):
        Type = self.typeListbox.get(ACTIVE)
        Capacity = self.capacity.get()
        Building = self.buildingListbox.get(ACTIVE)
        Number = self.HNum.get()
    
        if Type and Capacity and Building and Number:
            name = Type + ' ' + Number + Building
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBasev8"
                )
                cursor = db.cursor()
                sql = "INSERT INTO location (name, capacity) VALUES (%s, %s)"
                cursor.execute(sql, (name, Capacity))
                db.commit()
                messagebox.showinfo("Registration Success", "Location registered successfully.")
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
            database="PDataBasev8"
        )
        cursor = db.cursor()
        cursor.execute("SELECT `ID`, `capacity`,  `name` FROM location ")
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
            database="PDataBasev8"
        )
        cursor = db.cursor()
        cursor.execute("DELETE FROM location WHERE ID = %s", (record_id,))
        db.commit()
        db.close()
        self.load_data()  

if __name__ == "__main__":
    root = Tk()
    app = LocationPageADD(root)
    root.mainloop()
