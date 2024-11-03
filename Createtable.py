from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from locationTable import LocationTable
from instructorTable import InstructorTable
from subjectData import Subject
from InstructorData import Instructor
from locationData import Location
class CreateTable:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Table")
        self.root.geometry('1600x1400')
        self.levels_dic = {}
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        self.time_slots = [
            "9:00 - 9:30", "9:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", 
            "11:00 - 11:30", "11:30 - 12:00", "12:00 - 12:30", "12:30 - 1:00", 
            "1:00 - 1:30", "1:30 - 2:00", "2:00 - 2:30", "2:30 - 3:00", 
            "3:00 - 3:30", "3:30 - 4:00", "4:00 - 4:30", "4:30 - 5:00"
        ]

        self.create_widgets()

    def create_widgets(self):
        label_style = {'font': ('Arial', 12, 'bold')}
        
        self.departments = self.fetch_departments()
        self.department_dict = {name: dept_id for dept_id, name in self.departments}

        self.input_frame = Frame(self.root)
        self.input_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")

        self.departmentLabel = Label(self.input_frame, text="Department:", **label_style)
        self.departmentLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.department = StringVar()
        self.departmentEntry = ttk.Combobox(self.input_frame, textvariable=self.department)
        self.departmentEntry['values'] = [name for name in self.department_dict.keys()]
        self.departmentEntry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.departmentEntry.bind("<<ComboboxSelected>>", self.load_levels)

        self.levelLabel = Label(self.input_frame, text="Level:", **label_style)
        self.levelLabel.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.level = IntVar()
        self.levelEntry = ttk.Combobox(self.input_frame, textvariable=self.level) 
        self.levelEntry.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        #self.levelEntry.bind("<<ComboboxSelected>>", self.load_subjects)

        self.createButton = Button(self.input_frame, text="Load", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.create_table)
        self.createButton.grid(row=2, column=0, columnspan=2, pady=5)

        self.subjectLabel = Label(self.input_frame, text="Subject:", **label_style)
        self.subjectLabel.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.subject = StringVar()
        self.subjectEntry = ttk.Combobox(self.input_frame, textvariable=self.subject)
        self.subjectEntry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        self.typeLabel = Label(self.input_frame, text="Type:", **label_style)
        self.typeLabel.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.type = StringVar()
        self.typeEntry = ttk.Combobox(self.input_frame, textvariable=self.type)
        self.typeEntry['values'] = ["Lecture", "Lab"]
        self.typeEntry.grid(row=4, column=1, padx=5, pady=5, sticky=W)
        self.typeEntry.bind("<<ComboboxSelected>>", self.instructorOfSubject)

        self.instructorLabel = Label(self.input_frame, text="Instructor:", **label_style)
        self.instructorLabel.grid(row=5, column=0, padx=5, pady=5, sticky=W)
        self.instructor = StringVar()
        self.instructor_listbox = ttk.Combobox(self.input_frame, textvariable=self.instructor)
        #Listbox(self.input_frame, selectmode=SINGLE, exportselection=0)
        self.instructor_listbox.grid(row=5, column=1, padx=5, pady=5, sticky=W)

        self.dayLabel = Label(self.input_frame, text="Day:", **label_style)
        self.dayLabel.grid(row=6, column=0, padx=5, pady=5, sticky=W)
        self.day = StringVar()
        self.dayEntry = ttk.Combobox(self.input_frame, textvariable=self.day)
        self.dayEntry['values'] = self.days
        self.dayEntry.grid(row=6, column=1, padx=5, pady=5, sticky=W)
        self.dayEntry.bind("<<ComboboxSelected>>", self.timeOfInstructor)

        self.startTimeLabel = Label(self.input_frame, text="Start Time (hour):", **label_style)
        self.startTimeLabel.grid(row=7, column=0, padx=5, pady=5 , sticky=W)
        self.startTime = StringVar()
        self.startTimeEntry = ttk.Combobox(self.input_frame, textvariable=self.startTime)
        self.startTimeEntry.grid(row=7, column=1, padx=5, pady=5, sticky=W)
        self.startTimeEntry.bind("<<ComboboxSelected>>", self.locationEmpty)

        self.sectionsFromLabel = Label(self.input_frame, text="From Section:", **label_style)
        self.sectionsFromLabel.grid(row=8, column=0, padx=5, pady=5, sticky=W)
        self.sectionsFrom = IntVar()
        self.sectionsFromEntry = Entry(self.input_frame, textvariable=self.sectionsFrom)
        self.sectionsFromEntry.grid(row=8, column=1, padx=5, pady=5, sticky=W)

        self.sectionsToLabel = Label(self.input_frame, text="To Section:", **label_style)
        self.sectionsToLabel.grid(row=9, column=0, padx=5, pady=5, sticky=W)
        self.sectionsTo = IntVar()
        self.sectionsToEntry = Entry(self.input_frame, textvariable=self.sectionsTo)
        self.sectionsToEntry.grid(row=9, column=1, padx=5, pady=5, sticky=W)
        
        self.locationLabel = Label(self.input_frame, text="Location:", **label_style)
        self.locationLabel.grid(row=10, column=0, padx=5, pady=5, sticky=W)
        self.location = StringVar()
        self.locationEntry = ttk.Combobox(self.input_frame, textvariable=self.location)
        self.locationEntry.grid(row=10, column=1, padx=5, pady=5, sticky=W)

        self.addSubjectButton = Button(self.input_frame, text="Add Subject", bg='lightgreen', fg='black', font=('Arial', 12, 'bold'), command=self.add_subject_to_table)
        self.addSubjectButton.grid(row=11, column=0, columnspan=2, pady=20)

        self.instructorPageButton = Button(self.input_frame, text="Instructor Page", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.open_instructor_page)
        self.instructorPageButton.grid(row=12, column=0, pady=10)

        self.locationPageButton = Button(self.input_frame, text="Location Page", bg='lightblue', fg='black', font=('Arial', 12, 'bold'), command=self.open_location_page)
        self.locationPageButton.grid(row=12, column=1, pady=10)



        self.table_frame_outer = Frame(self.root)
        self.table_frame_outer.grid(row=0, column=0, sticky="nsew")

        self.table_canvas = Canvas(self.table_frame_outer)
        self.table_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar_v = Scrollbar(self.table_frame_outer, orient=VERTICAL, command=self.table_canvas.yview)
        self.scrollbar_v.pack(side=RIGHT, fill=Y)
        self.scrollbar_h = Scrollbar(self.table_frame_outer, orient=HORIZONTAL, command=self.table_canvas.xview)
        self.scrollbar_h.pack(side=BOTTOM, fill=X)

        self.table_canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)

        self.table_frame = Frame(self.table_canvas)
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor='nw')

        self.table_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=4)
        self.root.grid_columnconfigure(1, weight=1)    

    def locationEmpty(self, event):
        day = self.day.get()
        index_slot = self.time_slots.index(self.startTimeEntry.get())
        locations = []
        for location in self.locationsData.values():
            if location.time[day][self.time_slots[index_slot]] == 0 and location.time[day][self.time_slots[index_slot+1]] == 0 and location.time[day][self.time_slots[index_slot+2]] == 0 and location.time[day][self.time_slots[index_slot+3]] == 0:
                locations.append(location.name)
        
        self.locationEntry['values'] = locations

    def timeOfInstructor(self, event):
        self.location.set('')
        self.locationEntry['values'] = []
        subject_id = self.subjects[self.subject.get()]
        slots = []
        type = self.type.get()
        day = self.day.get()
        dr_id = self.instructorsByName[self.instructor.get()]
        length = len(self.time_slots)-3
        for i in range(length):
            if type == "Lecture":
                if self.drData[dr_id].time[day][self.time_slots[i]] == 0 and self.drData[dr_id].time[day][self.time_slots[i+1]] == 0 and self.drData[dr_id].time[day][self.time_slots[i+2]] == 0 and self.drData[dr_id].time[day][self.time_slots[i+3]] == 0 :
                    slots.append(self.time_slots[i])
            else:
                if self.TAData[dr_id].time[day][self.time_slots[i]] == 0 and self.TAData[dr_id].time[day][self.time_slots[i+1]] == 0 and self.TAData[dr_id].time[day][self.time_slots[i+2]] == 0 and self.TAData[dr_id].time[day][self.time_slots[i+3]] == 0 :
                    slots.append(self.time_slots[i])
        self.startTimeEntry['values'] = slots

    def instructorOfSubject(self, event):
        #["Lecture", "Lab"]
        self.instructor.set('')
        self.day.set('')
        self.startTime.set('')
        self.startTimeEntry['values'] = []
        self.location.set('')
        self.locationEntry['values'] = []
        subject_id = self.subjects[self.subject.get()]
        type = self.type.get()
        instructorsList = []
        if type == "Lecture":
            for drID in self.subjectsData[subject_id].dr:
                if self.drData[drID].load[subject_id]['done'] < self.drData[drID].load[subject_id]['load']: 
                    instructorsList.append([self.drData[drID].name])
        else:
            for TAID in self.subjectsData[subject_id].TA:
                if self.TAData[TAID].load[subject_id]['done'] < self.TAData[TAID].load[subject_id]['load']: 
                    instructorsList.append([self.TAData[TAID].name])
        
        self.instructor_listbox['values'] = instructorsList


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
        dept_id = self.department_dict[self.department.get()]
        self.levels = {}
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='PDataBaseV8'
            )
            cursor = connection.cursor()
            query_levels = "SELECT ID, levelNo, No_sections FROM level WHERE Dept_ID = %s"
            cursor.execute(query_levels, (dept_id,))
            levels = cursor.fetchall()
            self.levels = {level_no: {'id': level_id, 'sections': no_sections} for level_id, level_no, no_sections in levels}
            self.levelEntry['values'] = list(self.levels.keys())
            #self.levelEntry.set('')  # Clear the current selection
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def load_subjects(self, event=None):
        level_no = self.level.get()
        self.level_id = self.levels.get(level_no, {}).get('id')
        if self.level_id is None:
            return
        self.subjects = {}
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='PDataBaseV8'
            )
            cursor = connection.cursor()
            query_subjects = "SELECT ID, Name FROM subject WHERE level_ID = %s"
            cursor.execute(query_subjects, (self.level_id,))
            subjects = cursor.fetchall()
            self.subjects = {subj_name: subj_id for subj_id, subj_name in subjects}
            self.subjectsData={subj_id: Subject(subj_name,self.sections) for subj_id, subj_name in subjects}
            self.subjectEntry['values'] = list(self.subjects.keys())
            self.subjectEntry.set('')  # Clear the current selection
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def load_instructors(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='PDataBaseV8'
            )
            cursor = connection.cursor()
            query_instructors = "SELECT ID, Name, Role FROM instructor"
            cursor.execute(query_instructors)
            instructors = cursor.fetchall()
            self.drData = {}
            self.TAData = {}
            self.instructorsByName = {}
            for id, name, role in instructors:
                self.instructorsByName[name] = id
                if role == "Dr":
                    self.drData[id] = Instructor(name, self.days, self.time_slots)
                else:
                    self.TAData[id] = Instructor(name, self.days, self.time_slots)
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_locations(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT ID, Name FROM location")
            rows = cursor.fetchall()
            self.locationsData={id: Location(name, self.days, self.time_slots) for id, name in rows}
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []
        
    def load_locations(self):
        self.locations = self.fetch_locations()
        self.location_dict = {name: loc_id for loc_id, name in self.locations}
        self.locationEntry.set('')

    def create_table(self, event=None):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        level = self.level.get()
        department = self.department.get()
        self.sections = self.levels.get(level, {}).get('sections', 0)

        title = f"Level {level} - {department}"
        titleLabel = Label(self.table_frame, text=title, font=('Arial', 16, 'bold'))
        titleLabel.grid(row=0, column=0, columnspan=len(self.time_slots) + 2, pady=10)

        Label(self.table_frame, text="Day", borderwidth=1, relief="solid", width=10).grid(row=1, column=0, sticky="nsew")
        Label(self.table_frame, text="Sections", borderwidth=1, relief="solid", width=15).grid(row=1, column=1, sticky="nsew")

        for col, time_slot in enumerate(self.time_slots):
            Label(self.table_frame, text=time_slot, borderwidth=1, relief="solid", width=15).grid(row=1, column=col+2, sticky="nsew")

        current_row = 2
        for day in self.days:
            day_label = Label(self.table_frame, text=day, borderwidth=1, relief="solid", width=10)
            day_label.grid(row=current_row, column=0, rowspan=self.sections, sticky="nsew")

            for section in range(1, self.sections + 1):
                Label(self.table_frame, text=f"Section {section}", borderwidth=1, relief="solid", width=15).grid(row=current_row, column=1, sticky="nsew")

                for col in range(1, len(self.time_slots) + 1):
                    entry = Entry(self.table_frame, width=15, borderwidth=1, relief="solid")
                    entry.grid(row=current_row, column=col+1, sticky="nsew")

                current_row += 1

            separator = Frame(self.table_frame, bg='black', height=2, bd=1, relief="solid")
            separator.grid(row=current_row, column=0, columnspan=len(self.time_slots) + 2, sticky="nsew", pady=(5, 5))

            current_row += 1

        for col in range(len(self.time_slots) + 2):
            self.table_frame.columnconfigure(col, weight=1)
        for row in range(current_row):
            self.table_frame.rowconfigure(row, weight=1)

        self.subject.set('')
        self.type.set('')
        self.instructor.set('')
        self.day.set('')
        self.startTime.set('')
        self.location.set('')
        self.load_subjects()
        self.load_instructors()
        self.load_locations()
        self.load_Loading()
        self.load_schedule()


    def load_schedule(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT ID, level_ID, subject_ID, instructor_ID, Location_ID, Day, sections, time_start FROM schedule")
            rows = cursor.fetchall()
            for ID, level_ID, subject_ID, instructor_ID, Location_ID, Day, sections, time_start in rows:
                subject_type = "Lecture" if instructor_ID in self.drData.keys() else "Lab"
                if subject_type == "Lecture":
                    instructor = self.drData[instructor_ID].name
                else:
                    instructor = self.TAData[instructor_ID].name
                
                sectionsList = str(sections).split(',')
                sections_from = int(sectionsList[0])
                sections_to = int(sectionsList[len(sectionsList)-1])
                self.draw(time_start, Day, self.subjectsData[subject_ID].name, subject_type, instructor, self.locationsData[Location_ID].name, sections_from, sections_to)
                #Location
                index = self.time_slots.index(time_start)
                for i in range(4):
                    self.locationsData[Location_ID].time[Day][self.time_slots[index+i]] = 1
                #instructor and subject
                
                if instructor_ID in self.drData.keys():
                    self.drData[instructor_ID].load[subject_ID]['done'] +=1
                    for i in range(4):
                        self.drData[instructor_ID].time[Day][self.time_slots[index+i]] = 1
                    
                    for s in sectionsList:
                        self.subjectsData[subject_ID].lecture[int(s)] = True
                else:
                    self.TAData[instructor_ID].load[subject_ID]['done'] +=1
                    for i in range(4):
                        self.TAData[instructor_ID].time[Day][self.time_slots[index+i]] = 1
                    for s in sectionsList:
                        self.subjectsData[subject_ID].section[int(s)] = True
                
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def load_Loading(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            cursor = db.cursor()
            cursor.execute("SELECT instructor_ID, subject_ID, No_sections FROM instructorload")
            rows = cursor.fetchall()
            for instructor_ID, subject_ID, No_sections in rows:
                if instructor_ID in self.drData.keys():
                    self.drData[instructor_ID].load[subject_ID] = {"load": No_sections, "done": 0}
                    self.subjectsData[subject_ID].dr.append(instructor_ID)
                else:
                    self.TAData[instructor_ID].load[subject_ID] = {"load": No_sections, "done": 0}
                    self.subjectsData[subject_ID].TA.append(instructor_ID)
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_subject_to_table(self):
        try:
            day = self.day.get()
            start_time = self.startTime.get()
            sections_from = self.sectionsFrom.get()
            sections_to = self.sectionsTo.get()
            subject = self.subjects[self.subject.get()]
            instructor = self.instructorsByName[self.instructor.get()]
            location = self.location_dict[self.location.get()]
            subject_type = self.type.get()
            sections = str(sections_from)

            if sections_from > sections_to:
                messagebox.showinfo("Faild", "start section must be less than end section.")
                return
            
            if sections_from > self.sections or sections_to > self.sections:
                messagebox.showinfo("Faild", "sections out of the range (1, "+ str(self.sections)+")")
                return

            for i in range(sections_from, sections_to+1):
                if subject_type == "Lecture":
                    if(self.subjectsData[subject].lecture[i] == True):
                        messagebox.showinfo("Faild", "section "+str(i)+" already exist.")
                        return
                else:
                    if(self.subjectsData[subject].section[i] == True):
                        messagebox.showinfo("Faild", "section "+str(i)+" already exist.")
                        return
            no_section = (sections_to+1) - sections_from
            if subject_type == "Lecture":
                load = self.drData[instructor].load[subject]['load'] - self.drData[instructor].load[subject]['done']
                if no_section > load:
                    messagebox.showinfo("Faild", "This instructor has "+str(load)+" left.")
                    return
            else:
                load = self.TAData[instructor].load[subject]['load'] - self.TAData[instructor].load[subject]['done']
                if no_section > load:
                    messagebox.showinfo("Faild", "This instructor has "+str(load)+" left.")
                    return
            for i in range(sections_from+1, sections_to+1):
                sections += ","+str(i)

            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBaseV8"
            )
            
            cursor = db.cursor()
            sql = """
                INSERT INTO schedule (level_ID, subject_ID, instructor_ID, Location_ID, Day, sections, time_start)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(sql, (self.level_id, subject, instructor, location, day, sections, start_time))
            db.commit()
            instructorName = ""
            if subject_type == "Lecture":
                instructorName = self.drData[instructor].name
            else:
                instructorName = self.TAData[instructor].name
            self.draw(start_time, day, self.subjectsData[subject].name, subject_type, instructorName, self.locationsData[location].name, sections_from, sections_to)

            #subject
            for i in range(sections_from, sections_to+1):
                if subject_type == "Lecture":
                    self.subjectsData[subject].lecture[i] = True
                else:
                    self.subjectsData[subject].section[i] = True
            #instructor
            index = self.time_slots.index(start_time)
            if subject_type == "Lecture":
                self.drData[instructor].load[subject]['done'] += no_section
                for i in range(4):
                    self.drData[instructor].time[day][self.time_slots[index+i]] = 1
            else:
                self.TAData[instructor].load[subject]['done'] += no_section
                for i in range(4):
                    self.TAData[instructor].time[day][self.time_slots[index+i]] = 1
            #location
            for i in range(4):
                self.locationsData[location].time[day][self.time_slots[index+i]] = 1
            #reset
            self.instructor.set('')
            self.instructor_listbox['values'] = []
            self.day.set('')
            self.sectionsFrom.set('')
            self.sectionsTo.set('')
            self.startTime.set('')
            self.startTimeEntry['values'] = []
            self.location.set('')
            self.locationEntry['values'] = []
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            # Ensure the database connection is always closed
            if db.is_connected():
                db.close()

    def draw(self, start, day, subject, subject_type, instructor, location, sections_from, sections_to):
        # GUI code to update the table (unchanged)
        start_col = self.time_slots.index(start) + 2
        end_col = start_col + 4
        day_index = self.days.index(day)
        day_row_start = 1 + (day_index * self.sections) + day_index

        cell_content = f"{subject}\n{subject_type}\n{instructor}\n{location}"
        label = Label(self.table_frame, text=cell_content,
            font=('Arial', 12, 'bold'), borderwidth=1, relief="solid",
            anchor='center', justify='center')
        label.grid(row=day_row_start + sections_from, column=start_col, 
                columnspan=4, rowspan=sections_to+1 - sections_from, sticky="nsew")

        for col in range(start_col, end_col):
            self.table_frame.grid_columnconfigure(col, weight=1)
        for row in range(day_row_start + sections_from, (day_row_start + sections_to+1)):
            self.table_frame.grid_rowconfigure(row, weight=1)

    def open_instructor_page(self):
        new_window = Toplevel(self.root)
        InstructorTable(new_window)

    def open_location_page(self):
        new_window = Toplevel(self.root)
        LocationTable(new_window)
if __name__ == "__main__":
    root = Tk()
    app = CreateTable(root)
    root.mainloop()
