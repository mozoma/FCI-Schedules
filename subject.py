from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Subject:
    def __init__(self, root):
        self.root = root
        self.root.title("Subject")
        self.root.geometry('600x400')
        self.root.configure(bg='lightblue')
        self.levels_dic = {}

        label_style = {'bg': 'lightblue', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
        entry_style = {'font': ('Arial', 12)}

        self.department = self.fetch_departments()
        self.department_dict = {name: level_id for level_id, name in self.department}

        # Labels and Entry widgets
        self.departmentLabel = Label(root, text="Department:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentLabel.grid(row=0, column=0)
        self.departmentVar = StringVar()
        self.departmentEntry = ttk.Combobox(root, textvariable=self.departmentVar)
        self.departmentEntry['values'] = [name for name in self.department_dict.keys()]
        self.departmentEntry.grid(row=0, column=1, padx=10, pady=10)
        self.departmentEntry.bind("<<ComboboxSelected>>", self.load_levels)

        self.levelLabel = Label(root, text="Level:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.levelLabel.grid(row=1, column=0)
        self.levelVar = StringVar()
        self.levelEntry = ttk.Combobox(root, textvariable=self.levelVar)
        self.levelEntry.grid(row=1, column=1, padx=10, pady=10)

        self.nameLabel = Label(root, text="Name:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.nameLabel.grid(row=2, column=0)
        self.nameVar = StringVar()
        self.nameEntry = Entry(root, width=20, textvariable=self.nameVar)
        self.nameEntry.grid(row=2, column=1, padx=10, pady=10)

        self.timePerWeekLabel = Label(root, text="Time per week:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.timePerWeekLabel.grid(row=3, column=0)
        self.timePerWeekVar = IntVar()
        self.timePerWeekEntry = Entry(root, width=20, textvariable=self.timePerWeekVar)
        self.timePerWeekEntry.grid(row=3, column=1, padx=10, pady=10)

        self.sectionHourLabel = Label(root, text="Section hour:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.sectionHourLabel.grid(row=4, column=0)
        self.sectionHourVar = IntVar()
        self.sectionHourEntry = Entry(root, width=20, textvariable=self.sectionHourVar)
        self.sectionHourEntry.grid(row=4, column=1, padx=10, pady=10)

        self.lectureHourLabel = Label(root, text="Lecture hour:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.lectureHourLabel.grid(row=5, column=0)
        self.lectureHourVar = IntVar()
        self.lectureHourEntry = Entry(root, width=20, textvariable=self.lectureHourVar)
        self.lectureHourEntry.grid(row=5, column=1, padx=10, pady=10)

        self.submitButton = Button(self.root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=6, column=0, columnspan=2, pady=20)

        self.loadButton = Button(self.root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=7, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=('ID', 'level_ID', 'Name', 'Time_per_week', 'Sectionhour', 'Lecturehour'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('level_ID', text='Level ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Time_per_week', text='Time per Week')
        self.tree.heading('Sectionhour', text='Section Hour')
        self.tree.heading('Lecturehour', text='Lecture Hour')
        self.tree.grid(row=8, column=0, columnspan=2, pady=20)

        self.deleteButton = Button(self.root, text="Delete Record", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_record)
        self.deleteButton.grid(row=9, column=0, columnspan=2, pady=10)

        self.load_data()

    def fetch_departments(self):
        db = mysql.connector.connect(
            host="localhost",
            user='root',
            password='',
            database="PDataBasev8"
        )
        cursor = db.cursor()
        cursor.execute("SELECT ID , Name FROM `department`")  # Adjust the table and columns as per your database schema
        rows = cursor.fetchall()
        db.close()
        return rows

    def insert_to_db(self):
        level_ID = self.levels_dic[int(self.levelVar.get())]
        name = self.nameVar.get()
        time_per_week = self.timePerWeekVar.get()
        section_hour = self.sectionHourVar.get()
        lecture_hour = self.lectureHourVar.get()

        if level_ID and name and time_per_week and section_hour and lecture_hour:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBasev8"
                )
                cursor = db.cursor()
                sql = "INSERT INTO Subject (level_ID, Name, Times_per_week, Sectionhour, Lecturehour) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (level_ID, name, time_per_week, section_hour, lecture_hour))
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
            database="PDataBasev8"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Subject")
        rows = cursor.fetchall()
        db.close()
        return rows

    def load_levels(self,event):
        self.levels_dic.clear()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='PDataBasev8'
            )
            cursor = connection.cursor()
            # Load levels and sections
            dept_id=self.department_dict[self.departmentVar.get()]
            dept_id=str(dept_id)
            query_levels = "SELECT ID,  levelNo FROM level WHERE Dept_ID = " + dept_id
            cursor.execute(query_levels)
            data = cursor.fetchall()
            self.levels_dic = {levelNo: ID for ID,levelNo in data}
            self.levelEntry['values'] = [levelNo for levelNo in self.levels_dic.keys()]
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.fetch_data()
        for row in rows:
            self.tree.insert("", END, values=row)

    def delete_record(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return

        selected_item = selected_items[0]
        values = self.tree.item(selected_item, 'values')
        record_id = values[0]  # Assuming the ID is the first column

        if not record_id:
            messagebox.showwarning("Selection Error", "Failed to get record ID. Please try again.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBasev8"
            )
            cursor = db.cursor()
            
            # Delete the referencing rows in the InstructorLoad table first
            cursor.execute("DELETE FROM InstructorLoad WHERE subject_ID = %s", (record_id,))
            
            # Now delete the row in the Subject table
            cursor.execute("DELETE FROM Subject WHERE ID = %s", (record_id,))
            
            db.commit()
            db.close()

            # Remove the item from the Treeview
            self.tree.delete(selected_item)

            messagebox.showinfo("Success", "Record deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


if __name__ == "__main__":
    root = Tk()
    app = Subject(root)
    root.mainloop()
