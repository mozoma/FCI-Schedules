from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class Load:
    def __init__(self, root):
        self.root = root
        self.root.title("Load Management")
        self.root.geometry('600x600')
        self.root.configure(bg='lightblue')

        # Fetch data from instructor table
        self.instructor_dict = {}
        self.departments = self.fetch_departments()
        self.department_dict = {name: dept_id for dept_id, name in self.departments}
        self.levels_dic = {}

        # Role
        self.roleLabel = Label(root, text="Role:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.roleLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.roleVar = StringVar()
        self.roleEntry = ttk.Combobox(root, textvariable=self.roleVar)
        self.roleEntry['values'] = ["Dr", "TA"]
        self.roleEntry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.roleEntry.bind("<<ComboboxSelected>>", self.fetch_instructors)

        # Instructor
        self.instructortidLabel = Label(root, text="Instructor:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.instructortidLabel.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.instructortidVar = StringVar()
        self.instructortidEntry = ttk.Combobox(root, textvariable=self.instructortidVar)
        self.instructortidEntry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        # Department
        self.departmentLabel = Label(root, text="Department:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.departmentLabel.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.department = StringVar()
        self.departmentEntry = ttk.Combobox(root, textvariable=self.department)
        self.departmentEntry['values'] = [name for name in self.department_dict.keys()]
        self.departmentEntry.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        self.departmentEntry.bind("<<ComboboxSelected>>", self.load_levels)

        # Level
        self.levelLabel = Label(root, text="Level:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.levelLabel.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.level = IntVar()
        self.levelEntry = ttk.Combobox(root, textvariable=self.level) 
        self.levelEntry.grid(row=3, column=1, padx=10, pady=10, sticky=W)
        self.levelEntry.bind("<<ComboboxSelected>>", self.fetch_subjects)

        # Subject
        self.subjectLabel = Label(root, text="Subject:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.subjectLabel.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.subjectVar = StringVar()
        self.subjectEntry = ttk.Combobox(root, textvariable=self.subjectVar)
        self.subjectEntry.grid(row=4, column=1, padx=10, pady=10, sticky=W)

        # Sections
        self.sectionsLabel = Label(root, text="Number of Sections:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.sectionsLabel.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        self.sectionsVar = IntVar()
        self.sectionsEntry = Entry(root, textvariable=self.sectionsVar)
        self.sectionsEntry.grid(row=5, column=1, padx=10, pady=10, sticky=W)

        # Submit Button
        self.submitButton = Button(root, text="Submit", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.insert_to_db)
        self.submitButton.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

        # Load Data Button
        self.loadButton = Button(root, text="Load Data", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.load_data)
        self.loadButton.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Treeview for displaying data
        self.tree = ttk.Treeview(root, columns=('instructor', 'subject', 'sections'), show='headings')
        self.tree.heading('instructor', text='Instructor')
        self.tree.heading('subject', text='Subject')
        self.tree.heading('sections', text='Sections')
        self.tree.grid(row=8, column=0, columnspan=2, padx=10, pady=20)

        # Delete Button
        self.deleteButton = Button(root, text="Delete", bg='red', fg='white', font=('Arial', 12, 'bold'), command=self.delete_from_db)
        self.deleteButton.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def fetch_instructors(self, event):
        self.instructor_dict.clear()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            role = self.roleVar.get()
            cursor = db.cursor()
            sql = "SELECT ID, Name FROM instructor WHERE Role = %s" 
            cursor.execute(sql, (role,))
            rows = cursor.fetchall()
            self.instructor_dict = {name: instructor_id for instructor_id, name in rows}
            self.instructortidEntry['values'] = [name for name in self.instructor_dict.keys()]
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

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
        
    def load_levels(self, event):
        self.levels_dic.clear()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='PDataBaseV8'
            )
            cursor = connection.cursor()
            dept_id = self.department_dict[self.department.get()]
            query_levels = "SELECT ID, levelNo, No_sections FROM level WHERE Dept_ID = %s"
            cursor.execute(query_levels, (dept_id,))
            data = cursor.fetchall()
            self.levels_dic = {levelNo: [ID, No_sections] for ID, levelNo, No_sections in data}
            self.levelEntry['values'] = [levelNo for levelNo in self.levels_dic.keys()]
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_subjects(self, event):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            id = self.levels_dic[self.level.get()][0]
            cursor.execute("SELECT ID, Name FROM subject WHERE level_ID = %s", (id,))
            rows = cursor.fetchall()
            self.subject_dict = {Name: ID for ID, Name in rows}
            self.subjectEntry['values'] = [Name for Name in self.subject_dict.keys()]
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def insert_to_db(self):
        instr_id = self.instructor_dict[self.instructortidVar.get()]
        subj_id = self.subject_dict[self.subjectVar.get()]
        No_sections = self.sectionsVar.get()

        if instr_id and subj_id and No_sections:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    database="PDataBaseV8"
                )
                cursor = db.cursor()

                level_id = self.levels_dic[self.level.get()][0]
                cursor.execute("SELECT No_sections FROM level WHERE ID = %s", (level_id,))
                level_data = cursor.fetchone()
                if level_data:
                    total_sections = level_data[0]
                    cursor.execute("SELECT SUM(No_sections) FROM instructorload WHERE subject_ID = %s", (subj_id,))
                    taken_sections = cursor.fetchone()[0] or 0
                    remaining_sections = total_sections - taken_sections
                    if No_sections > remaining_sections:
                        messagebox.showerror("Input Error", f"Error: Only {remaining_sections} sections left in this level.")
                    else:
                        sql = "INSERT INTO instructorload (instructor_ID, subject_ID, No_sections) VALUES (%s, %s, %s)"
                        val = (instr_id, subj_id, No_sections)
                        cursor.execute(sql, val)
                        db.commit()
                        self.load_data()
                        messagebox.showinfo("Success", "Data inserted successfully.")
                db.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showerror("Input Error", "Please fill in all fields.")

    def load_data(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute(
                """
                SELECT instructor.Name, subject.Name, instructorload.No_sections
                FROM instructorload
                JOIN instructor ON instructorload.instructor_ID = instructor.ID
                JOIN subject ON instructorload.subject_ID = subject.ID
                """
            )
            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def delete_from_db(self):
        selected_item = self.tree.selection()[0]
        instructor_name = self.tree.item(selected_item, 'values')[0]
        subject_name = self.tree.item(selected_item, 'values')[1]

        instr_id = self.instructor_dict[instructor_name]
        subj_id = self.subject_dict[subject_name]

        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            sql = "DELETE FROM instructorload WHERE instructor_ID = %s AND subject_ID = %s"
            cursor.execute(sql, (instr_id, subj_id))
            db.commit()
            db.close()
            self.load_data()
            messagebox.showinfo("Success", "Record deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    root = Tk()
    app = Load(root)
    root.mainloop()
