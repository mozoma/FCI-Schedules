from tkinter import *
from tkinter import messagebox
from main import MainPage
import mysql.connector

class Login:
    def __init__(self, master):
        self.master = master
        self.master.title('Login Form')
        self.master.geometry('400x200')

        self.usernameLabel = Label(self.master, text="User Name")
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.username = StringVar()
        self.usernameEntry = Entry(self.master, textvariable=self.username)
        self.usernameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.passwordLabel = Label(self.master, text="Password")
        self.passwordLabel.grid(row=1, column=0, padx=10, pady=10)
        self.password = StringVar()
        self.passwordEntry = Entry(self.master, textvariable=self.password, show='*')
        self.passwordEntry.grid(row=1, column=1, padx=10, pady=10)

        self.loginButton = Button(self.master, text="Login", command=self.logintodb)
        self.loginButton.grid(row=2, column=1, pady=10)

    def logintodb(self):
        UName = self.username.get()
        Pass = self.password.get()
        try:
            db = mysql.connector.connect(
                host="localhost",
                user='root',
                password='',
                database="PDataBasev8"
            )
            cursor = db.cursor()
            sql = "SELECT * FROM login WHERE UName=%s AND Pass=%s"
            cursor.execute(sql, (UName, Pass))
            myresult = cursor.fetchall()
            if myresult:
                messagebox.showinfo("Login Success")
                self.open_main_page()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def open_main_page(self):
        self.master.destroy()
        main_page = Tk()
        MainPage(main_page)

if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()



