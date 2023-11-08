#Assignment 1 - SQLite
import sqlite3
import csv

# a. function to import students.csv file into students table
path_to_database = './StudentDB.db'
conn = sqlite3.connect(path_to_database) #establish connection to db
mycursor = conn.cursor() #cursor allows python to execute SQL statements

def import_data():
    path_to_csv = './students.csv'
    with open(path_to_csv, newline='') as csvfile:
        read_item = csv.reader(csvfile, delimiter=',')
        i = 1
        no = 0
        faculty = "N/A"
        next(read_item)
        for row in read_item:
            mycursor.execute("INSERT INTO Student VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                             (i, row[0], row[1], row[8], row[7], faculty, row[2], row[3], row[4], row[5], row[6], no))
            i += 1
        conn.commit()  # make sure consistent
    mycursor.close()
    print("CSV imported")

# b. display all students and attributes (select statement)]
def display_all():
    mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0")
    table = mycursor.fetchall()
    for row in table:
        print(row)

# c. Add new student
def add_student():
    #StudentID
    mycursor.execute("SELECT MAX(StudentID) FROM Student")
    result = mycursor.fetchone()
    studentid = int(result[0]) + 1

    #first name
    print("Type Student First Name: ")
    first_name = input()

    #last name
    print("Type Student Last Nane: ")
    last_name = input()

    #gpa
    while True:
        print("Type Student's GPA: ")
        gpa = input()
        try:
            gpa = float(gpa)
            #checking if too high of a number for a gpa
            if gpa < 5.0:
                break
            else:
                print("GPA value not valid. Try again.")
        except ValueError:
            print("Input not valid. Try again.")

    #major
    print("Type Student's Major: ")
    major = input()

    #faculty
    print("Type Faculty Advisory: ")
    faculty = input()

    #address
    print("Type Address of where the student lives: ")
    address = input()

    #city
    print("Type City of where the student lives: ")
    city = input()

    #state
    print("Type State of where the student lives: ")
    state = input()

    #zipcode
    print("Type Zipcode of where the student lives: ")
    zipcode = input()

    #phone number
    print("Type Student's Mobile Phone Number: ")
    phone_number = input()

    #isDeleted
    delete = 0

    mycursor.execute("INSERT INTO Student VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (studentid, first_name, last_name, gpa, major, faculty, address, city, state, zipcode, phone_number, delete))
    conn.commit()
    print("New Student Added.")

# d. Update students
def update_students():
    #Student ID - checks to make sure valid ID
    while True:
        print("State the Student ID of the Student that you would like to update: ")
        student = input()
        try:
            student = int(student)
            break
        except ValueError:
            print("Input not valid. Try again.")

    # Checking if Student exists in the table
    mycursor.execute("SELECT * FROM Student WHERE StudentID = (?)", (student,))
    table = mycursor.fetchall()
    if not table:
        print("Student Does not Exist.")
    #Updates Student if the StudentID exists
    else:
        while True:
            print("Would you like to update the student's major, advisor, or mobile phone number?")
            field = input()
            if field.lower() == "major":
                print("Type the updated major:")
                major = input().title()
                mycursor.execute("UPDATE Student SET Major = (?) WHERE StudentID = (?)", (major, student))
                conn.commit()
                print("Student's Major was updated.")
                break
            elif field.lower() == "advisor":
                print("Type the Faculty Advisor:")
                advisor = input().title()
                mycursor.execute("UPDATE Student SET FacultyAdvisor = (?) WHERE StudentID = (?)", (advisor, student))
                conn.commit()
                print("Student's Faculty Advisor was updated.")
                break
            elif field.lower() == "phone number" or field.lower() == "mobile phone number":
                print("Type the Mobile Phone Number:")
                number = input()
                mycursor.execute("UPDATE Student SET MobilePhoneNumber = (?) WHERE StudentID = (?)", (number, student))
                conn.commit()
                print("Student's Mobile Phone Number was updated.")
                break
            else:
                print("Not a valid field to update. Try again.")

# e. Delete students by StudentID
def delete_student():
    print("Provide the Student ID of the Student you would like to delete.")
    student = int(input())
    mycursor.execute("SELECT * FROM Student WHERE StudentID = (?)", (student,))
    table = mycursor.fetchall()
    if not table:
        print("Student does not exist, cannot be deleted.")
    else:
        mycursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = (?)",(student,))
        conn.commit()
        print("Student was deleted.")

# f. Search for Students by Major, GPA, City, State and Advisor.
def search_students():
    print("Specify how you would like to search for Students by Major, GPA, City, State, and Advisor?")
    search = input()
    #searching making sure only searching through the students that were not soft deleted

    #search by major
    if search.lower() == "major":
        print("Insert Major: ")
        major = input().title()
        mycursor.execute("SELECT * FROM Student WHERE Major = (?) AND isDeleted = 0", (major,))
        table = mycursor.fetchall()
        if not table:
            print("No Search Results found.")
        else:
            for row in table:
                print(row)
    #search by gpa
    elif search.lower() == "gpa":
        while True:
            print("Insert GPA: ")
            gpa = input()
            try:
                gpa = float(gpa)
                break
            except ValueError:
                print("GPA invalid. Try Again.")
        mycursor.execute("SELECT * FROM Student WHERE GPA = (?) AND isDeleted = 0",(gpa,))
        table = mycursor.fetchall()
        if not table:
            print("No Search Results found.")
        else:
            for row in table:
                print(row)
    #search by city
    elif search.lower() == "city":
        print("Insert City: ")
        city = input().title()
        mycursor.execute("SELECT * FROM Student WHERE City = (?) AND isDeleted = 0", (city,))
        table = mycursor.fetchall()
        if not table:
            print("No Search Results found.")
        else:
            for row in table:
                print(row)
    #search by state
    elif search.lower() == "state":
        print("Insert State: ")
        state = input().title()
        mycursor.execute("SELECT * FROM Student WHERE State = (?) AND isDeleted = 0", (state,))
        table = mycursor.fetchall()
        if not table:
            print("No Search Results found.")
        else:
            for row in table:
                print(row)
    #search by advisor
    elif search.lower() == "advisor":
        print("Insert Advisor: ")
        advisor = input().title()
        mycursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = (?) AND isDeleted = 0", (advisor,))
        table = mycursor.fetchall()
        if not table:
            print("No Search Results found.")
        else:
            for row in table:
                print(row)
    #no search field correct
    else:
        print("Invalid Search Field.")
        search_students()

#Options for the application
def operations(option):
    if option == 1:
        #display all students not deleted
        display_all()
    elif option == 2:
        #add a student
        add_student()
    elif option == 3:
        #update student
        update_students()
    elif option == 4:
        # deletes a student based on student id
        delete_student()
    elif option == 5:
        #Search for a student based on a certain field
        search_students()
    else:
        print("Invalid Operation. Try Again.")

def app_run():
    print("Type the number of the operation you would like to execute. If you want to exit the application, type 'EXIT'")
    print("OPTIONS: ")
    print("1 - Display All Student Information")
    print("2 - Add a New Student")
    print("3 - Update Student Information")
    print("4 - Delete a Student")
    print("5 - Search for a Student")
    print("6 - EXIT\n")
    answer = input()
    while int(answer) != 6:
        operations(int(answer))
        print("\nType the number of the operation you would like to execute. If you want to exit the application, type 'EXIT'")
        print("OPTIONS: ")
        print("1 - Display All Student Information")
        print("2 - Add a New Student")
        print("3 - Update Student Information")
        print("4 - Delete a Student")
        print("5 - Search for a Student")
        print("6 - EXIT")
        answer = input()
    mycursor.close()

#import_data()
app_run()



