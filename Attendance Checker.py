from tkinter import *
from tkinter import font
import pymysql
from tkinter import ttk
import qrcode
from io import BytesIO
from tkinter import messagebox
import datetime
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import sys

#This is the Main Window(Login Page)
class MainSystem(Tk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Monitoring System")
        self.geometry("1536x864")
        self.state('zoomed')

        self.conn = self.connect_to_database()
        self.bg = PhotoImage(file="login_system_design.png")
        self.custom_font = font.Font(family="Courier New", size=20, weight="bold")
        self.custom_font1 = font.Font(family="Courier New", size=12, weight="bold")
        self.hex_color = "#F1EAFF"
        self.label = Label(self, image=self.bg).place(x=0, y=0)
        self.widgets()

    def widgets(self):
        self.frame1 = Frame(self, width=500, height=500, bg=self.hex_color)
        self.frame1.place(x=1000, y=250)

        self.lbl = Label(self.frame1, text="Login", font=self.custom_font, fg="purple", bg=self.hex_color)
        self.lbl.grid(column=0,columnspan=4, row=0, pady=40, sticky="ew",padx=20)

        self.lbl_username = Label(self.frame1, text="Username:", font=self.custom_font1, fg="purple", bg=self.hex_color)
        self.lbl_username.grid(column=1, row=2,padx=20)

        self.lbl_password = Label(self.frame1, text="Password:", font=self.custom_font1, fg="purple", bg=self.hex_color)
        self.lbl_password.grid(column=1, row=3,padx=20,pady=15)

        self.entry_username = Entry(self.frame1)
        self.entry_username.grid(column=2, row=2,padx=20)

        self.entry_password = Entry(self.frame1, show="*")
        self.entry_password.grid(column=2, row=3, padx=20,pady=15)

        self.btn_login = Button(self.frame1, text="Sign In", font=self.custom_font1, command=self.login_user,
                                fg="white", bg="purple")
        self.btn_login.grid(column=0,columnspan=4, row=4, pady=40,padx=20)

    def connect_to_database(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='dbStudRecords'
        )
        return self.conn

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        cursor = self.conn.cursor()

        select_query = "SELECT * FROM tbUsers WHERE username=%s AND password=%s"
        user_data = (username, password)

        try:
            cursor.execute(select_query, user_data)
            result = cursor.fetchone()

            if result:
                print("Account Found")
                self.login_page()
            else:
                print("Account not Found")
        except:
            pass
        finally:
            cursor.close()
    def login_page(self):
        self.withdraw()
        Home()

#Home Page (Display For Student Infos ,Attendance Buttons with Different Functions)
class Home(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Home Page")
        self.geometry("1536x864")
        self.state('zoomed')
        self.widgets()
        self.toggle_menu()

        self.tree = None

    def widgets(self):
        self.head_frame = Frame(self, bg='#F1EAFF', highlightbackground='Purple', highlightthickness=1)
        self.head_frame.pack(side=TOP, fill=X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=50)


        self.toggle_btn = Button(self.head_frame, text='≡', bg='#F1EAFF', fg='Purple', font=('Bold', 30), bd=0,
                               activebackground='#F1EAFF', activeforeground='#fff', command=self.toggle_menu)
        self.toggle_btn.pack(side=LEFT)

        self.title_lbl = Label(self.head_frame, text='Attendance Checker', bg='#F1EAFF', fg='Purple', font=('Bold', 20), bd=0,
                             activebackground='#F1EAFF', activeforeground='#fff')
        self.title_lbl.pack(side=LEFT)


        self.scan_btn = Button(self.toggle_menu_fm, text='Scan', font=('Bold', 20), bd=0, bg='#F1EAFF', fg='Purple',
                             activebackground='#F1EAFF', activeforeground='#fff',command=Scanner)

        self.scan_btn.place(x=20, y=20)


        self.info_btn = Button(self.toggle_menu_fm, text='Info', font=('Bold', 20), bd=0, bg='#F1EAFF', fg='Purple',
                             activebackground='#F1EAFF', activeforeground='#fff',command=self.show_info)
        self.info_btn.place(x=20, y=80)


        self.logout_btn = Button(self.toggle_menu_fm, text='Exit', font=('Bold', 20), bd=0, bg='#F1EAFF', fg='Purple',
                               activebackground='#F1EAFF', activeforeground='#fff',command=self.logout)
        self.logout_btn.place(x=20, y=140)


    def toggle_menu(self):
        def collapse_toggle_menu():
            self.toggle_menu_fm.destroy()
            self.toggle_btn.config(text='≡', command=self.toggle_menu)

        self.toggle_menu_fm = Frame(self, bg='#F1EAFF', highlightbackground='Purple', highlightthickness=1)
        self.window_height = 864
        self.toggle_menu_fm.place(x=0, y=50, height=self.window_height, width=200)
        self.toggle_btn.config(command=collapse_toggle_menu)


        self.scan_btn = Button(self.toggle_menu_fm, text='Scan', font=('Bold', 20), bd=0, bg='#F1EAFF', fg='Purple',
                                 activebackground='#F1EAFF', activeforeground='#fff',command=Scanner)
        self.scan_btn.place(x=20, y=20)

        self.info_btn = Button(self.toggle_menu_fm, text='Info', font=('Bold', 20), bd=0, bg='#F1EAFF', fg='Purple',
                                 activebackground='#F1EAFF', activeforeground='#fff',command=self.show_info)
        self.info_btn.place(x=20, y=80)

        self.logout_btn = Button(self.toggle_menu_fm, text='Exit', font=('Bold', 20), bd=0, bg='#F1EAFF', fg='Purple',
                                   activebackground='#F1EAFF', activeforeground='#fff',command=self.logout)
        self.logout_btn.place(x=20, y=140)

    def logout(self):
        self.destroy()
        sys.exit()

    def connect_to_database(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='dbStudRecords'
        )
        return self.conn

    def show_info(self):
        self.FrameStud = Frame(self, bd=4, relief=RIDGE, bg="#F1EAFF")
        self.FrameStud.place(x=270, y=100, width=1200, height=630)
        # Create a treeview for tabular display
        self.tree = ttk.Treeview(self.FrameStud, columns=('Student ID', 'Name', 'Section', 'Course'), show='headings')

        self.tree.heading('Student ID', text='Student ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Section', text='Section')
        self.tree.heading('Course', text='Course')
        self.tree.pack(fill='both', expand=True)

        #Buttons of View the Attendance,Generate QrCode,Reload,Delete,Edit
        self.btn1 = Button(self,bg='purple',fg='white',text="View the Attendance", command=self.view)
        self.btn1.place(x=272, y=65)
        self.btn2 = Button(self,bg='purple',fg='white',text="Generate QrCode", command=QrCode)
        self.btn2.place(x=392, y=65)
        self.btn3 = Button(self,bg='purple',fg='white', text="Reload", command=self.Reload)
        self.btn3.place(x=494, y=65)
        self.btn3 = Button(self, bg='purple', fg='white', text="Delete",command=self.Delete)
        self.btn3.place(x=541, y=65)
        self.btn4 = Button(self, bg='purple', fg='white', text="Edit", command=self.Update)
        self.btn4.place(x=585, y=65)

        #Connect the database
        self.connect_to_database()
        self.cursor = self.conn.cursor()

        #Get the data from the table qr_codes
        self.cursor.execute('SELECT studNum, name, section, course FROM qr_codes')
        self.res = self.cursor.fetchall()


        for row in self.tree.get_children():
            self.tree.delete(row)

        rows_by_studnum = {}

        for row in self.res:
            studnum = row[0]
            if studnum in rows_by_studnum:
                self.tree.item(rows_by_studnum[studnum], values=row)
            else:
                self.tree.insert('', 'end', values=row)
                rows_by_studnum[studnum] = self.tree.get_children()[-1]

    def view(self):
        self.notif = Toplevel()
        self.notif.title("View the Attendance")
        self.notif.geometry("300x100")
        self.notif.resizable(False, False)
        self.notif.configure(bg='#F1EAFF')
        self.customfont = font.Font(family="Courier New", size=12, weight="bold")
        lblview = Label(self.notif,bg='#F1EAFF',fg='purple', font=self.customfont ,text="Enter the Student Number: ")
        lblview.grid(column=0,row=0 ,padx=20)
        global entr
        entr = Entry(self.notif)
        entr.grid(column=0,row=1,padx=20)
        btnView = Button(self.notif, text="Submit",font=self.customfont,bg='purple',fg='white', command=self.showAttendance)
        btnView.grid(column=0,row=2,padx=20, pady=10)

    def showAttendance(self):
        ans = entr.get()
        self.FrameAtten = Frame(self, bd=4, relief=RIDGE, bg="#F1EAFF")
        self.FrameAtten.place(x=270, y=100, width=1200, height=630)

        self.tree_attendance = ttk.Treeview(self.FrameAtten, columns=('No.','Student Number', 'Attendance', 'Entry Time'), show='headings')

        self.tree_attendance.heading('No.', text='No.')
        self.tree_attendance.heading('Student Number', text='Student Number')
        self.tree_attendance.heading('Attendance', text='Attendance')
        self.tree_attendance.heading('Entry Time', text='Entry Time')
        self.tree_attendance.pack(fill='both', expand=True)

        if ans:
            self.cursor.execute(f'SELECT * FROM attendanceMonitor WHERE student="{ans}"')
        else:
            self.show_info()
            messagebox.showinfo("View the Attendance", "Enter the Student Number!")
        self.ress = self.cursor.fetchall()
        for row in self.tree_attendance.get_children():
            self.tree_attendance.delete(row)


        rows_by_student = {}

        for row in self.ress:
            student = row[0]
            if student in rows_by_student:
                self.tree_attendance.item(rows_by_student[student], values=row)
            else:
                self.tree_attendance.insert('', 'end', values=row)
                rows_by_student[student] = self.tree_attendance.get_children()[-1]
        self.notif.destroy()

    def Reload(self):
        self.show_info()

    def Delete(self):
        self.notif1 = Toplevel()
        self.notif1.title("Delete Data")
        self.notif1.geometry("300x100")
        self.notif1.resizable(False, False)
        self.notif1.configure(bg='#F1EAFF')
        self.customfont2 = font.Font(family="Courier New", size=12, weight="bold")
        lbldel = Label(self.notif1, bg='#F1EAFF', fg='purple', font=self.customfont2, text="Enter the Student Number: ")
        lbldel.grid(column=0, row=0, padx=20)
        global entrdel
        entrdel = Entry(self.notif1)
        entrdel.grid(column=0, row=1, padx=20)
        btndel = Button(self.notif1, text="Submit", font=self.customfont2, bg='purple', fg='white',
                         command=self.DeleteFunc)
        btndel.grid(column=0, row=2, padx=20, pady=10)

    def DeleteFunc(self):
        ans1 = entrdel.get()

        self.connect_to_database()
        self.cursor = self.conn.cursor()

        if ans1:
            self.cursor.execute(f"DELETE FROM qr_codes WHERE studNum='{ans1}'")
            self.cursor.execute(f"DELETE FROM attendanceMonitor WHERE student='{ans1}'")
            messagebox.showinfo("Delete Data", "Deleted Successfully!")
        else:
            messagebox.showinfo("Delete Data", "Enter the Student Number!")
        self.conn.commit()
        self.conn.close()
        self.notif1.destroy()

    def Update(self):
        self.notif2 = Toplevel()
        self.notif2.title("Edit Data")
        self.notif2.geometry("500x250")
        self.notif2.resizable(False, False)
        self.notif2.configure(bg='#F1EAFF')
        self.customfont3 = font.Font(family="Courier New", size=12, weight="bold")
        self.lblupdate = Label(self.notif2, bg='#F1EAFF', fg='purple', font=self.customfont3,
                                 text="Enter the Student Number:")
        self.lblupdate.grid(column=0, row=0, padx=15, pady=12)
        self.entryupdate = Entry(self.notif2)
        self.entryupdate.grid(column=1, columnspan=3, row=0, sticky='ew')

        self.lblupdate1 = Label(self.notif2, font=self.customfont3, bg='#F1EAFF', fg='purple', text="Enter the Name: ")
        self.lblupdate1.grid(column=0, row=1, padx=15, pady=12)
        self.entryupdate1 = Entry(self.notif2)
        self.entryupdate1.grid(column=1, columnspan=3, row=1, sticky='ew')

        self.lblupdate2 = Label(self.notif2, font=self.customfont3, bg='#F1EAFF', fg='purple', text="Enter the Section: ")
        self.lblupdate2.grid(column=0, row=2, padx=15, pady=12)
        self.entryupdate2 = Entry(self.notif2)
        self.entryupdate2.grid(column=1, columnspan=3, row=2, sticky='ew')

        self.lblupdate3 = Label(self.notif2, font=self.customfont3, bg='#F1EAFF', fg='purple', text="Enter the Course:")
        self.lblupdate3.grid(column=0, row=3, padx=15, pady=12)
        self.entryupdate3 = Entry(self.notif2)
        self.entryupdate3.grid(column=1, columnspan=3, row=3, sticky='ew')


        self.updatebutton = Button(self.notif2, font=self.customfont3, bg='purple', fg='white', text="Submit",
                                      command=self.UpdateFunc)
        self.updatebutton.grid(column=0, columnspan=4, row=4, pady=15, padx=140)

    def UpdateFunc(self):
        self.studNum = self.entryupdate.get()
        self.name = self.entryupdate1.get()
        self.section = self.entryupdate2.get()
        self.course = self.entryupdate3.get()

        self.connect_to_database()

        self.cursor = self.conn.cursor()

        if self.studNum:
            self.cursor.execute(f"UPDATE qr_codes SET name='{self.name}', section='{self.section}', course='{self.course}' WHERE studNum='{self.studNum}'")
            self.conn.commit()
            self.conn.close()
            messagebox.showinfo("Edit Data", "Edited Successfully!")
            self.notif2.destroy()
        else:
            messagebox.showinfo("Edit Data", "Enter all the necessary data!")
            self.notif2.destroy()

#Qr Code Scanner
class Scanner():
    def __init__(self):
        super().__init__()
        self.scan_qr_code()

    def connect_to_database(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='dbStudRecords'
        )
        return self.conn

    def mark_attendance(self, data):
        now = datetime.now()
        entry_time = now.strftime("%Y-%m-%d %H:%M:%S")
        attendance = "Present"
        self.connect_to_database()
        self.cursor = self.conn.cursor()

        self.cursor.execute('INSERT INTO attendanceMonitor (student, entry_time, attendance) VALUES (%s, %s, %s)',
                           (data, entry_time, attendance))
        self.conn.commit()

        messagebox.showinfo("Attendance Marked", f"Successfully marked attendance for QR code: {data}")

    def scan_qr_code(self):
        # Open the camera
        cap = cv2.VideoCapture(0)

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Decode QR codes
            decoded_objects = decode(frame)

            # Display the frame
            cv2.imshow("QR Code Scanner", frame)

            # Check for QR codes in the frame
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                self.mark_attendance(data)

            # The camera will close by clicking 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # the camera and the window will close
        cap.release()
        cv2.destroyAllWindows()

#Qr Code Generator
class QrCode(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Generate QrCode")
        self.geometry("450x250")
        self.resizable(False,False)
        self.configure(bg='#F1EAFF')
        self.widgets()

    def connect_to_database(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='dbStudRecords'
        )
        return self.conn

    def generate_qr(self):
        self.studNum = self.entry.get()
        self.name = self.entry1.get()
        self.section = self.entry2.get()
        self.course = self.entry3.get()

        self.connect_to_database()

        self.cursor = self.conn.cursor()
        self.conn.commit()

        if self.studNum:
            # Generate QR code
            self.qr = qrcode.make(self.studNum)
            # Save QR code image
            self.img_bytes = BytesIO()
            self.qr.save(self.img_bytes)
            self.img_bytes.seek(0)

            self.qr.save("studinfos/" + str(self.studNum) + ".png")


            self.cursor.execute('INSERT INTO qr_codes (studNUm,name,section,course,image) VALUES (%s, %s, %s, %s, %s)',
                           (self.studNum, self.name, self.section, self.course, self.img_bytes.read()))
            self.conn.commit()

            messagebox.showinfo("QR Code Generator", "QR Code generated and saved successfully!")
            self.withdraw()
        else:
            messagebox.showerror("QR Code Generator", "Please enter data.")
            self.destroy()

    def widgets(self):
        self.customfont1 = font.Font(family="Courier New", size=10, weight="bold")

        self.entry_label = Label(self,bg='#F1EAFF',fg='purple', font= self.customfont1, text="Enter the Student Number:")
        self.entry_label.grid(column=0, row=0,padx=15,pady=12)
        self.entry = Entry(self)
        self.entry.grid(column=1,columnspan=3, row=0,sticky='ew')

        self.entry_label1 = Label(self,font= self.customfont1,bg='#F1EAFF',fg='purple', text="Enter the Name: ")
        self.entry_label1.grid(column=0, row=1,padx=15,pady=12)
        self.entry1 = Entry(self)
        self.entry1.grid(column=1,columnspan=3, row=1,sticky='ew')

        self.entry_label2 = Label(self,font= self.customfont1,bg='#F1EAFF',fg='purple', text="Enter the Section: ")
        self.entry_label2.grid(column=0, row=2,padx=15,pady=12)
        self.entry2 = Entry(self)
        self.entry2.grid(column=1,columnspan=3, row=2,sticky='ew')

        self.entry_label3 = Label(self,font= self.customfont1,bg='#F1EAFF',fg='purple', text="Enter the Course:")
        self.entry_label3.grid(column=0, row=3,padx=15,pady=12)
        self.entry3 = Entry(self)
        self.entry3.grid(column=1,columnspan=3, row=3,sticky='ew')

        self.generate_button = Button(self,font= self.customfont1,bg='purple',fg='white', text="Generate QR Code", command=self.generate_qr)
        self.generate_button.grid(column=0,columnspan=4, row=4, pady=15,padx=140)

#Run the Main Window
main=MainSystem()
main.mainloop()


