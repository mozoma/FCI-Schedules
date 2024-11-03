import mysql.connector
from tkinter import messagebox

class DatabaseModel:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "PDataBaseV8"
        }

    def connect(self):
        return mysql.connector.connect(**self.db_config)

    def fetch_departments(self):
        try:
            db = self.connect()
            cursor = db.cursor()
            cursor.execute("SELECT ID, Name FROM department")
            rows = cursor.fetchall()
            db.close()
            return rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def insert_level(self, dept_id, level_no, no_sections):
        try:
            db = self.connect()
            cursor = db.cursor()
            sql = "INSERT INTO level (Dept_ID, levelNo, No_sections) VALUES (%s, %s, %s)"
            cursor.execute(sql, (dept_id, level_no, no_sections))
            db.commit()
            db.close()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return False

    def fetch_levels(self):
        try:
            db = self.connect()
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

    def delete_level(self, record_id):
        try:
            db = self.connect()
            cursor = db.cursor()
            cursor.execute("DELETE FROM level WHERE id = %s", (record_id,))
            db.commit()
            db.close()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return False
  
