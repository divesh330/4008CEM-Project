from tkinter import *
from ast import Delete
import tkinter as tk
from tkinter import ttk, messagebox

import sqlite3

root = Tk()
root.geometry("1632x626")

# ENTRIES

global bookingIDTextField
global lecturerIDTextField
global bookingClassTextField
global bookingMonthTextField
global bookingDateTextField
global bookingStartTextField
global bookingEndTextField
global noOfStudentsTextField

bookingIDTextField = Entry(root)
lecturerIDTextField = Entry(root)
bookingClassTextField = Entry(root)
bookingMonthTextField = Entry(root)
bookingDateTextField = Entry(root)
bookingStartTextField = Entry(root)
bookingEndTextField = Entry(root)
noOfStudentsTextField = Entry(root)


# FUNCTIONS
def display():

    # HEADERS
    cols = ('Booking ID', 'Lecturer ID', 'Booking Class', 'Booking Month', 'Booking Date', 'Booking Start Time',
            'Booking End Time', 'Number of Students')

    listBox = ttk.Treeview(root, columns=cols, show='headings')

    for col in cols:
        listBox.heading(col, text=col)
        listBox.grid(row=1, column=0, columnspan=1)
        listBox.place(x=10, y=10)

    listBox.bind('<Double-Button-1>', GetValue)

    # CONTENT
    conn = sqlite3.connect("classroom.db")
    cursor = conn.cursor()

    query = "SELECT * from Booking"
    cursor.execute(query)
    records = cursor.fetchall()

    print('records')
    print(records)
    for row, (BookingID, BStime, BClass, BEtime, BDay, BMonth, ClassID, LectureID, Student) in enumerate(records, start=1):
        listBox.insert("", "end", values=(
            BookingID, LectureID, BClass, BMonth, BDay, BStime, BEtime, Student))


def Clear():
    bookingIDTextField.delete(0, END)
    lecturerIDTextField.delete(0, END)
    bookingClassTextField.delete(0, END)
    bookingMonthTextField.delete(0, END)
    bookingDateTextField.delete(0, END)
    bookingStartTextField.delete(0, END)
    bookingEndTextField.delete(0, END)
    noOfStudentsTextField.delete(0, END)

    bookingIDTextField.focus_set()

    display()


def Modify():
    bookingID = bookingIDTextField.get()

    try:
        conn = sqlite3.connect("classroom.db")
        cursor = conn.cursor()

        query = '''SELECT * from Booking where BookingID = '%s' ''' % bookingID
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)

        if result is None:
            messagebox.showinfo(
                "Information", "Booking ID %s doesn't exist" % bookingID)
            Clear()

        else:
            Clear()
            lecturerIDTextField.insert(0, result[7])
            bookingClassTextField.insert(0, result[2])
            bookingMonthTextField.insert(0, result[5])
            bookingDateTextField.insert(0, result[4])
            bookingStartTextField.insert(0, result[1])
            bookingEndTextField.insert(0, result[3])
            noOfStudentsTextField.insert(0, result[8])
            bookingIDTextField.insert(0, result[0])

    except sqlite3.Error as error:
        messagebox.showinfo("Error", "Error retrieving data %s" % error)


def Update():
    bookingID = bookingIDTextField.get()
    lecturerID = lecturerIDTextField.get()
    bookingClass = bookingClassTextField.get()
    bookingMonth = bookingMonthTextField.get()
    bookingDate = bookingDateTextField.get()
    bookingStart = bookingStartTextField.get()
    bookingEnd = bookingEndTextField.get()
    noOfStudents = noOfStudentsTextField.get()

    try:
        conn = sqlite3.connect('classroom.db')
        cursor = conn.cursor()

        query = '''UPDATE Booking set LectureID = '%s', BStime = %s, BClass = '%s', BEtime = %s, BDay = '%s', BMonth = '%s', 'No.Of.Student' = %s where BookingID = '%s' ''' % (
            lecturerID, bookingStart, bookingClass, bookingEnd, bookingDate, bookingMonth, noOfStudents, bookingID)

        cursor.execute(query)
        conn.commit()
        conn.close()
        messagebox.showinfo("Information", "Updated data successfully")
        Clear()

    except sqlite3.Error as error:
        messagebox.showinfo(
            "Error", "Failed to update data into sqlite table %s" % error)


def Delete():
    bookingID = bookingIDTextField.get()

    try:
        conn = sqlite3.connect("classroom.db")
        cursor = conn.cursor()

        query = '''DELETE from Booking where BookingID = '%s' ''' % (
                bookingID)
        cursor.execute(query)
        conn.commit()
        conn.close()

        if(cursor.rowcount <= 0):
            messagebox.showinfo(
                "Failed", "Booking ID %s doesn't exist" % bookingID)
        else:
            messagebox.showinfo(
                "Successful", "Record deleted successfully %s" % bookingID)
        Clear()
    except sqlite3.Error as error:
        messagebox.showinfo("Error", "Error deleting data")

# UI ONLY


Label(root, text="Modify a booking slot",
      font=(None, 18)).place(x=10, y=250)


Label(root, text="Booking ID").place(x=10, y=300)
bookingIDTextField.place(x=100, y=300)
Button(root, text="Modify", command=Modify,
       height=0, width=10).place(x=250, y=295)
Button(root, text="Delete", command=Delete,
       height=0, width=10).place(x=350, y=295)


Label(root, text="Lecturer ID").place(x=10, y=350)
lecturerIDTextField.place(x=100, y=350)

Label(root, text="Booking Class").place(x=250, y=350)
bookingClassTextField.place(x=350, y=350)

Label(root, text="Month").place(x=10, y=400)
bookingMonthTextField.place(x=100, y=400)

Label(root, text="Date \n(DD/MM/YYYY)").place(x=250, y=392)
bookingDateTextField.place(x=350, y=400)

Label(root, text="Start Time").place(x=10, y=450)
bookingStartTextField.place(x=100, y=450)

Label(root, text="End Time").place(x=250, y=450)
bookingEndTextField.place(x=350, y=450)

Label(root, text="Number of Students").place(x=480, y=450)
noOfStudentsTextField.place(x=600, y=450)

Button(root, text="Update", command=Update,
       height=0, width=10).place(x=10, y=500)

Button(root, text="Clear", command=Clear,
       height=0, width=10).place(x=100, y=500)


def GetValue(event):
    print('whatever')


display()
root.mainloop()
