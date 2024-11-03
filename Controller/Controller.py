from model import DatabaseModel
from view import LevelView
from tkinter import messagebox

class LevelController:
    def __init__(self, root):
        self.model = DatabaseModel()
        self.view = LevelView(root, self)
        self.load_departments()

    def load_departments(self):
        departments = self.model.fetch_departments()
        if departments:
            self.view.populate_departments(departments)

    def submit_record(self):
        department_name = self.view.departmentidVar.get()
        department_dict = {name: dept_id for dept_id, name in self.model.fetch_departments()}
        dept_id = department_dict.get(department_name)
        level_no = self.view.levelVar.get()
        no_sections = self.view.sectionsVar.get()

        if dept_id and level_no and no_sections:
            if self.model.insert_level(dept_id, level_no, no_sections):
                messagebox.showinfo("Success", "Record inserted successfully.")
                self.load_data()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def load_data(self):
        rows = self.model.fetch_levels()
        if rows:
            self.view.populate_tree(rows)

    def delete_record(self):
        record = self.view.get_selected_record()
        if record:
            record_id = record[0]
            if self.model.delete_level(record_id):
                messagebox.showinfo("Success", "Record deleted successfully.")
                self.load_data()
