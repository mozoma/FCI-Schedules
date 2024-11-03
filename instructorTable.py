from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class InstructorTable:
    def __init__(self, master):
        self.master = master
        self.master.title('Instructor Schedule')
        self.master.geometry('1000x600')
        self.master.configure(bg='lightblue')
        self.time_slots = [
            "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00",
            "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 1:00",
            "1:00 - 1:30", "1:30 - 2:00", "2:00 - 2:30", "2:30 - 3:00",
            "3:00 - 3:30", "3:30 - 4:00", "4:00 - 4:30", "4:30 - 5:00"
        ]
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

        self.instructor_dict = {}
        self.setup_widgets()
        self.fetch_subjects()
        self.fetch_locations()

    def setup_widgets(self):
        self.roleLabel = Label(self.master, text="Role:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.roleLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.roleVar = StringVar()
        self.roleEntry = ttk.Combobox(self.master, textvariable=self.roleVar)
        self.roleEntry['values'] = ["Dr", "TA"]
        self.roleEntry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.roleEntry.bind("<<ComboboxSelected>>", self.fetch_instructors)

        self.instructortidLabel = Label(self.master, text="Instructor:", bg='lightblue', font=('Arial', 12, 'bold'))
        self.instructortidLabel.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.instructortidVar = StringVar()
        self.instructortidEntry = ttk.Combobox(self.master, textvariable=self.instructortidVar)
        self.instructortidEntry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        self.instructortidEntry.bind("<<ComboboxSelected>>", self.fetch_schedule)

        self.canvas = Canvas(self.master, bg='lightblue')
        self.canvas.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.scroll_x = Scrollbar(self.master, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.table_frame = Frame(self.canvas, bg='lightblue')
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.table_frame.bind("<Configure>", self.on_frame_configure)

        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fetch_locations(self):
        self.instructor_dict.clear()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            sql = "SELECT ID, Name FROM location"
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.location_dict = {id: name for id, name in rows}
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def fetch_subjects(self):
        self.instructor_dict.clear()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            sql = "SELECT ID, Name FROM subject"
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.subject_dict = {id: name for id, name in rows}
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

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
            sql = "SELECT ID, Name FROM Instructor WHERE Role = %s"
            cursor.execute(sql, (role,))
            rows = cursor.fetchall()
            self.instructor_dict = {name: instructor_id for instructor_id, name in rows}
            self.instructortidEntry['values'] = [name for name in self.instructor_dict.keys()]
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_schedule(self, event=None):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        instructor_name = self.instructortidVar.get()
        instructor_id = self.instructor_dict.get(instructor_name)
        
        if instructor_id is None:
            messagebox.showerror("Error", "Instructor not selected")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            sql = "SELECT  subject_ID,  Location_ID, Day, time_start FROM schedule WHERE instructor_ID = %s"
            cursor.execute(sql, (instructor_id,))
            rows = cursor.fetchall()
            db.close()

            self.display_schedule(rows)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def display_schedule(self, schedule_data):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        Label(self.table_frame, text="Day", borderwidth=1, relief="solid", width=10).grid(row=1, column=0, sticky="nsew")
        for col, time_slot in enumerate(self.time_slots):
            Label(self.table_frame, text=time_slot, borderwidth=1, relief="solid", width=15).grid(row=1, column=col+2, sticky="nsew")

        current_row = 2
        for day in self.days:
            day_label = Label(self.table_frame, text=day, borderwidth=1, relief="solid", width=10)
            day_label.grid(row=current_row, column=0, rowspan=1, sticky="nsew")

            for col in range(1, len(self.time_slots) + 1):
                entry = Entry(self.table_frame, width=15, borderwidth=1, relief="solid")
                entry.grid(row=current_row, column=col+1, sticky="nsew")

            current_row += 1

        for subject_ID,  Location_ID, Day, time_start in schedule_data:
            start_col = self.time_slots.index(time_start) + 1
            day_index = self.days.index(Day)
            day_row_start = 2 + day_index 

            cell_content = f"{self.subject_dict[subject_ID]}\n{self.location_dict[Location_ID]}"
            label = Label(self.table_frame, text=cell_content,
                font=('Arial', 12, 'bold'), borderwidth=1, relief="solid",
                anchor='center', justify='center')
            label.grid(row=day_row_start, column=start_col, 
                columnspan=4, rowspan=1, sticky="nsew")

        for col in range(len(self.time_slots) + 1):
            self.table_frame.columnconfigure(col, weight=1)
        for row in range(1, current_row):
            self.table_frame.rowconfigure(row, weight=1)



if __name__ == "__main__":
    root = Tk()
    app = InstructorTable(root)
    root.mainloop()
