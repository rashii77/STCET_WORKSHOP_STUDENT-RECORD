import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("student.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
roll TEXT UNIQUE,
department TEXT,
year INTEGER,
gender TEXT,
email TEXT,
phone TEXT,
cgpa REAL
)
""")
conn.commit()

# -----------------------------
# Functions
# -----------------------------
def add_student(name, roll, department, year, gender, email, phone, cgpa):
    cursor.execute("""
    INSERT INTO students
    (name,roll,department,year,gender,email,phone,cgpa)
    VALUES(?,?,?,?,?,?,?,?)
    """,
    (name,roll,department,year,gender,email,phone,cgpa))
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return data


def search_student(roll):
    cursor.execute("SELECT * FROM students WHERE roll=?",(roll,))
    return cursor.fetchall()


def delete_student(roll):
    cursor.execute("DELETE FROM students WHERE roll=?",(roll,))
    conn.commit()


def update_student(name, roll, department, year, gender, email, phone, cgpa):
    cursor.execute("""
    UPDATE students
    SET name=?,
    department=?,
    year=?,
    gender=?,
    email=?,
    phone=?,
    cgpa=?
    WHERE roll=?
    """,
    (name,department,year,gender,email,phone,cgpa,roll))
    conn.commit()


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
page_title="Student Record Management System",
page_icon="🎓",
layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
"Home",
"Add Student",
"View Students",
"Search Student",
"Update Student",
"Delete Student"
]

choice = st.sidebar.selectbox("Menu",menu)

# -----------------------------
# Home
# -----------------------------
if choice=="Home":

    st.subheader("Dashboard")

    data=view_students()

    total=len(data)

    if total>0:
        df=pd.DataFrame(data,columns=[
        "ID","Name","Roll","Department","Year",
        "Gender","Email","Phone","CGPA"
        ])

        avg=df["CGPA"].mean()

        c1,c2=st.columns(2)

        c1.metric("Total Students",total)
        c2.metric("Average CGPA",round(avg,2))

        st.dataframe(df,use_container_width=True)

    else:
        st.info("No student records available.")

# -----------------------------
# Add
# -----------------------------
elif choice=="Add Student":

    st.subheader("Add Student")

    with st.form("add_form"):

        name=st.text_input("Student Name")
        roll=st.text_input("Roll Number")

        department=st.selectbox(
        "Department",
        [
        "Computer Science",
        "Mechanical",
        "Civil",
        "Electrical",
        "Electronics",
        "Information Technology",
        "MBA",
        "Other"
        ])

        year=st.selectbox("Year",[1,2,3,4])

        gender=st.radio("Gender",
        ["Male","Female","Other"])

        email=st.text_input("Email")
        phone=st.text_input("Phone")

        cgpa=st.slider(
        "CGPA",
        0.0,
        10.0,
        7.0,
        0.1
        )

        submit=st.form_submit_button("Add Student")

    if submit:

        try:
            add_student(
            name,
            roll,
            department,
            year,
            gender,
            email,
            phone,
            cgpa
            )

            st.success("Student Added Successfully!")

        except:
            st.error("Roll Number already exists.")

# -----------------------------
# View
# -----------------------------
elif choice=="View Students":

    st.subheader("Student Records")

    data=view_students()

    if len(data)>0:

        df=pd.DataFrame(data,columns=[
        "ID",
        "Name",
        "Roll",
        "Department",
        "Year",
        "Gender",
        "Email",
        "Phone",
        "CGPA"
        ])

        st.dataframe(df,use_container_width=True)

        csv=df.to_csv(index=False).encode()

        st.download_button(
        "Download CSV",
        csv,
        "students.csv",
        "text/csv"
        )

    else:
        st.warning("Database Empty.")

# -----------------------------
# Search
# -----------------------------
elif choice=="Search Student":

    st.subheader("Search Student")

    roll=st.text_input("Enter Roll Number")

    if st.button("Search"):

        result=search_student(roll)

        if result:

            df=pd.DataFrame(result,columns=[
            "ID",
            "Name",
            "Roll",
            "Department",
            "Year",
            "Gender",
            "Email",
            "Phone",
            "CGPA"
            ])

            st.dataframe(df,use_container_width=True)

        else:
            st.error("Student Not Found.")

# -----------------------------
# Update
# -----------------------------
elif choice=="Update Student":

    st.subheader("Update Student")

    roll=st.text_input("Enter Roll Number")

    if st.button("Load Student"):

        result=search_student(roll)

        if result:

            student=result[0]

            st.session_state.student=student

        else:
            st.error("Student Not Found")

    if "student" in st.session_state:

        s=st.session_state.student

        name=st.text_input("Name",s[1])

        department=st.text_input(
        "Department",
        s[3]
        )

        year=st.number_input(
        "Year",
        1,
        4,
        int(s[4])
        )

        gender=st.selectbox(
        "Gender",
        ["Male","Female","Other"],
        index=["Male","Female","Other"].index(s[5])
        )

        email=st.text_input("Email",s[6])

        phone=st.text_input("Phone",s[7])

        cgpa=st.number_input(
        "CGPA",
        0.0,
        10.0,
        float(s[8])
        )

        if st.button("Update"):

            update_student(
            name,
            s[2],
            department,
            year,
            gender,
            email,
            phone,
            cgpa
            )

            del st.session_state.student

            st.success("Student Updated Successfully.")

# -----------------------------
# Delete
# -----------------------------
elif choice=="Delete Student":

    st.subheader("Delete Student")

    roll=st.text_input("Enter Roll Number")

    if st.button("Delete"):

        result=search_student(roll)

        if result:

            delete_student(roll)

            st.success("Student Deleted Successfully.")

        else:

            st.error("Student Not Found.")
