import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# FUNCTIONS
def calculate_coursework_total(marks):
    return sum(marks)

def calculate_overall_percentage(coursework_total, exam_score):
    total_possible = 60 + 100
    return ((coursework_total + exam_score) / total_possible) * 100

def get_grade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

# LOAD STUDENT DATA
def load_student_data(filename=None):
    # A function that pretty much reads the text file that stores all the data/info of the students
    if filename is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, "assets", "studentMarks.txt")

    students = [] # to store student info
    try:
        with open(filename, "r") as file:
            num_students = int(file.readline().strip())
            for line in file:
                parts = line.strip().split(",")
                student_id = parts[0] # First value is the student ID
                name = parts[1] # Second value is the student name
                marks = list(map(int, parts[2:5]))
                exam_score = int(parts[5]) # Last value is the exam score

                # To calculate total coursework, overall percentage, and grade
                coursework_total = calculate_coursework_total(marks)
                overall_percentage = calculate_overall_percentage(coursework_total, exam_score)
                grade = get_grade(overall_percentage)

                students.append({
                    "id": student_id,
                    "name": name,
                    "marks": marks,
                    "exam": exam_score,
                    "coursework_total": coursework_total,
                    "percentage": overall_percentage,
                    "grade": grade
                })
        return students

    except FileNotFoundError:
        # Show an error if the file is not found
        messagebox.showerror("Error", f"File {filename} not found!")
        return []
    
def save_student_data(students, filename=None):
    # This rewrites the entire file whenever changes are done (saves updated changes)
    if filename is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, "assets", "studentMarks.txt")

    with open(filename, "w") as f:
        f.write(f"{len(students)}\n")
        for s in students:
            marks_str = ",".join(map(str, s["marks"]))
            f.write(f"{s['id']},{s['name']},{marks_str},{s['exam']}\n")


# MAIN APPLICATION
class StudentApp(tk.Tk):
    # Main window of the app
    def __init__(self, students):
        super().__init__()
        self.title("Student Management System")
        self.geometry("724x800")
        self.resizable(False, False)
        self.students = students # To store the student data

        # School icon for the app
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "assets", "icon.png")
        self.iconphoto(False, ImageTk.PhotoImage(file=icon_path))

        # Frame container
        # Holds all pages stacked on top of each other
        self.container = tk.Frame(self, bg="#4b1f24")
        self.container.pack(fill="both", expand=True)

        # PAGES
        self.frames = {} # Creates all pages at once and stores them in a dictionary
        for F in (
            MenuPage,
            AllStudentsPage,
            SelectStudentPage,
            StudentDetailPage,
            AddStudentPage,
            DeleteStudentPage,
            UpdateStudentPage,
            SortStudentsPage
        ):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        # Makes sure the menu page is shown first
        self.show_frame("MenuPage")

    # To switch to different pages
    def show_frame(self, name):
        self.frames[name].tkraise() # tkraise() lifts the chosen page to the top to make it visible


# PAGE HEADER
def add_header(parent):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # All pages contain the same header image for uniformity
    header_path = os.path.join(script_dir, "assets", "header.png")
    header_img = Image.open(header_path).resize((724, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(header_img)

    label = tk.Label(parent, image=photo, bg="#4b1f24")
    label.image = photo
    label.pack(fill="x")


# MENU PAGE
class MenuPage(tk.Frame): # Basically the homepage/main of the app
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="Student Management Menu",
                font=("Georgia", 26, "bold"), fg="white", bg="#4b1f24").pack(pady=25)

        btn_frame = tk.Frame(self, bg="#4b1f24")
        btn_frame.pack()

        # To create the buttons for the menu page
        def create_button(text, command):
            tk.Button(
                btn_frame, text=text, command=command,
                font=("Georgia", 12), bg="white", fg="#4b1f24",
                width=35, pady=10, relief="flat", cursor="hand2"
            ).pack(pady=5)

        create_button("View All Student Records",
                    lambda: controller.show_frame("AllStudentsPage"))
        create_button("View Individual Student Record",
                    lambda: controller.show_frame("SelectStudentPage"))
        create_button("Add a Student Record",
                    lambda: controller.show_frame("AddStudentPage"))
        create_button("Delete a Student Record",
                    lambda: controller.show_frame("DeleteStudentPage"))
        create_button("Update a Student Record",
                    lambda: controller.show_frame("UpdateStudentPage"))
        create_button("Sort Student Records",
                    lambda: controller.show_frame("SortStudentsPage"))
        create_button("Show Student with Highest Overall Mark",
                    self.show_highest)
        create_button("Show Student with Lowest Overall Mark",
                    self.show_lowest)

    # To show user the student with the HIGHEST percentage
    def show_highest(self):
        student = max(self.controller.students, key=lambda x: x["percentage"])
        self.controller.frames["StudentDetailPage"].set_student(student)
        self.controller.show_frame("StudentDetailPage")

    # To show user the student with the LOWEST percentage
    def show_lowest(self):
        student = min(self.controller.students, key=lambda x: x["percentage"])
        self.controller.frames["StudentDetailPage"].set_student(student)
        self.controller.show_frame("StudentDetailPage")


# ALL STUDENTS PAGE
class AllStudentsPage(tk.Frame):
    # I use ttk.Treeview to display info in a table
    # Info derived from PythonTutorial and GeeksforGeeks
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="All Student Records",
                font=("Georgia", 22, "bold"),
                bg="#4b1f24", fg="white").pack(pady=10)
        
        # Table columns to show complete info to user
        columns = (
            "Student ID", "Name", "Coursework Total",
            "Exam Score", "Overall Percentage", "Grade"
        )

        # Spreadsheet/table widget
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(pady=10)

        # Button to let user return to the menu/previous page
        tk.Button(self, text="Back to Menu", width=20,
                bg="white", fg="#4b1f24", cursor="hand2",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=10)

    # To update table every time page is shown. Learned from StackOverflow & GeeksforGeeks
    def tkraise(self, *args, **kwargs):
        self.tree.delete(*self.tree.get_children()) # Clears old data
        grade_colors = {
            "A": "#a8e6cf",
            "B": "#dcedc1",
            "C": "#fff9b0",
            "D": "#ffd3b6",
            "F": "#ff8b94"
        }
        for i, s in enumerate(self.controller.students):
            self.tree.insert("", tk.END, values=(
                s["id"], s["name"], s["coursework_total"],
                s["exam"], f"{s['percentage']:.2f}%", s["grade"]
            ))
            # Color-coded row based on the student's grade for organizational purposes
            item = self.tree.get_children()[-1]
            self.tree.tag_configure(f"grade{i}", background=grade_colors.get(s["grade"], "white"))
            self.tree.item(item, tags=(f"grade{i}",))
        super().tkraise(*args, **kwargs)


# SELECT STUDENT PAGE
class SelectStudentPage(tk.Frame):
    # Listbox is used in order to allow user to pick a student (Single)
    # Idea and info gathered from GeeksforGeeks & PythonTutorial
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="Select a Student",
                font=("Georgia", 22, "bold"),
                bg="#4b1f24", fg="white").pack(pady=10)

        # Contains a list of students with their ID number
        self.listbox = tk.Listbox(self, width=50, height=10)
        self.listbox.pack(pady=10)

        # Buttons to proceed or return to the page
        tk.Button(self, text="View Student Record", cursor="hand2",
                bg="white", fg="#4b1f24",
                command=self.view_student).pack(pady=5)

        tk.Button(self, text="Back to Menu", cursor="hand2",
                bg="white", fg="#4b1f24",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=5)

    def tkraise(self, *args, **kwargs):
        # This refreshes the Listbox to show the updated student names
        self.listbox.delete(0, tk.END)
        for s in self.controller.students:
            self.listbox.insert(tk.END, f"{s['id']} - {s['name']}")
        super().tkraise(*args, **kwargs)

    # This shows the info of the selected student
    def view_student(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Attention", "Please choose a student.")
            return
        student = self.controller.students[sel[0]]
        self.controller.frames["StudentDetailPage"].set_student(student)
        self.controller.show_frame("StudentDetailPage")


# STUDENT DETAIL PAGE
class StudentDetailPage(tk.Frame):
    # To show user the data for the student they've chosen in a small table
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="Student Record",
                font=("Georgia", 22, "bold"),
                bg="#4b1f24", fg="white").pack(pady=10)

        cols = ("Attribute", "Value")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=6)
        self.tree.heading("Attribute", text="Attribute")
        self.tree.heading("Value", text="Value")
        self.tree.column("Attribute", width=150, anchor="center")
        self.tree.column("Value", width=200, anchor="center")
        self.tree.pack(pady=20)

        tk.Button(self, text="Back to Menu",
                cursor="hand2", bg="white", fg="#4b1f24",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=10)

    # Display data for chosen student (single)
    def set_student(self, s):
        # Clears old data and inserts the info of the new student
        self.tree.delete(*self.tree.get_children())
        grade_colors = {
            "A": "#a8e6cf",
            "B": "#dcedc1",
            "C": "#fff9b0",
            "D": "#ffd3b6",
            "F": "#ff8b94"
        }

        data = [
            ("Name", s["name"]),
            ("Student ID", s["id"]),
            ("Coursework Total", s["coursework_total"]),
            ("Exam Mark", s["exam"]),
            ("Overall Percentage", f"{s['percentage']:.2f}%"),
            ("Grade", s["grade"]),
        ]

        for attr, value in data:
            self.tree.insert("", tk.END, values=(attr, value))
            # Grade row will only be colored to highlight the final grade
            if attr == "Grade":
                item = self.tree.get_children()[-1]
                self.tree.tag_configure("grade", background=grade_colors.get(value, "white"))
                self.tree.item(item, tags=("grade",))


# ADD STUDENT PAGE
class AddStudentPage(tk.Frame):
    # Where user types new student and their info
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="Add Student",
                font=("Georgia", 22, "bold"), fg="white",
                bg="#4b1f24").pack(pady=10)

        self.entries = {}
        labels = ["Student ID", "Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]

        for lbl in labels:
            tk.Label(self, text=lbl, fg="white", bg="#4b1f24", font=("Georgia", 12)).pack()
            entry = tk.Entry(self)
            entry.pack(pady=3)
            self.entries[lbl] = entry

        tk.Button(self, text="Add Student", bg="white", fg="#4b1f24",
                cursor="hand2", command=self.save).pack(pady=15)

        tk.Button(self, text="Back to Menu", bg="white", fg="#4b1f24",
                cursor="hand2",
                command=lambda: controller.show_frame("MenuPage")).pack()

    def save(self):
        # Collect data from entries and add the new student to the table/list
        try:
            marks = [
                int(self.entries["Coursework 1"].get()),
                int(self.entries["Coursework 2"].get()),
                int(self.entries["Coursework 3"].get())
            ]
            exam = int(self.entries["Exam Mark"].get())

            student = {
                "id": self.entries["Student ID"].get(),
                "name": self.entries["Name"].get(),
                "marks": marks,
                "exam": exam,
                "coursework_total": calculate_coursework_total(marks),
                "percentage": calculate_overall_percentage(calculate_coursework_total(marks), exam),
                "grade": get_grade(calculate_overall_percentage(calculate_coursework_total(marks), exam))
            }

            self.controller.students.append(student)
            save_student_data(self.controller.students)

            messagebox.showinfo("Success", "Student added successfully!")
            self.controller.show_frame("MenuPage")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks.")


# DELETE STUDENT PAGE
class DeleteStudentPage(tk.Frame):
    # From the Listbox, this allows user to delete chosen student
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="Delete Student Record",
                font=("Georgia", 22, "bold"), fg="white", bg="#4b1f24").pack(pady=10)

        self.listbox = tk.Listbox(self, width=50, height=12)
        self.listbox.pack(pady=10)

        tk.Button(self, text="Delete Selected",
                cursor="hand2", bg="white", fg="#4b1f24",
                command=self.delete_student).pack(pady=5)

        tk.Button(self, text="Back to Menu",
                cursor="hand2", bg="white", fg="#4b1f24",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=5)

    def tkraise(self, *args, **kwargs):
        self.listbox.delete(0, tk.END)
        for s in self.controller.students:
            self.listbox.insert(tk.END, f"{s['id']} - {s['name']}")
        super().tkraise(*args, **kwargs)

    def delete_student(self): # Removes chosen student from the list
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Attention", "Select a student to delete.")
            return

        student = self.controller.students.pop(sel[0])
        save_student_data(self.controller.students)
        messagebox.showinfo("Deleted", f"Student {student['name']} removed.")
        self.controller.show_frame("MenuPage")


# UPDATE STUDENT PAGE
class UpdateStudentPage(tk.Frame):
    # User will select a student first, then a form will appear to let them update or edit info/details
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="Update Student",
                font=("Georgia", 22, "bold"), bg="#4b1f24", fg="white").pack(pady=10)

        self.listbox = tk.Listbox(self, width=50, height=8)
        self.listbox.pack(pady=10)

        tk.Button(self, text="Edit Selected",
                cursor="hand2", bg="white", fg="#4b1f24",
                command=self.edit_student).pack(pady=5)

        self.form_frame = tk.Frame(self, bg="#4b1f24")
        self.form_frame.pack(pady=10)

        self.entries = {}

        tk.Button(self, text="Back to Menu",
                cursor="hand2", bg="white", fg="#4b1f24",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=5)

    def tkraise(self, *args, **kwargs):
        self.listbox.delete(0, tk.END)
        self.clear_form()

        for s in self.controller.students:
            self.listbox.insert(tk.END, f"{s['id']} - {s['name']}")
        super().tkraise(*args, **kwargs)

    def clear_form(self): # Deletes all form fields so that a new one appears to the user
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

    def edit_student(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Attention", "Select a student to update.")
            return

        self.selected = self.controller.students[sel[0]]
        self.clear_form()

        labels = ["Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]
        values = [self.selected["name"]] + self.selected["marks"] + [self.selected["exam"]]

        for lbl, val in zip(labels, values):
            tk.Label(self.form_frame, text=lbl, bg="#4b1f24", fg="white").pack()
            entry = tk.Entry(self.form_frame)
            entry.insert(0, str(val))
            entry.pack(pady=2)
            self.entries[lbl] = entry

        tk.Button(self.form_frame, text="Save Updates",
                cursor="hand2", bg="white", fg="#4b1f24",
                command=self.save_updates).pack(pady=10)

    def save_updates(self): # To save the updated details into the chosen student's info list
        try:
            self.selected["name"] = self.entries["Name"].get()
            self.selected["marks"] = [
                int(self.entries["Coursework 1"].get()),
                int(self.entries["Coursework 2"].get()),
                int(self.entries["Coursework 3"].get()),
            ]
            self.selected["exam"] = int(self.entries["Exam Mark"].get())

            self.selected["coursework_total"] = calculate_coursework_total(self.selected["marks"])
            self.selected["percentage"] = calculate_overall_percentage(
                self.selected["coursework_total"], self.selected["exam"]
            )
            self.selected["grade"] = get_grade(self.selected["percentage"])

            save_student_data(self.controller.students)

            messagebox.showinfo("Success", "Student updated successfully!")
            self.controller.show_frame("MenuPage")

        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers.")


# SORT STUDENTS PAGE
class SortStudentsPage(tk.Frame):
    # Basically sorts student based on their overall percentage (descending and ascending)
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        add_header(self)

        tk.Label(self, text="Sort Students",
                font=("Georgia", 22, "bold"),
                fg="white", bg="#4b1f24").pack(pady=10)

        tk.Button(
            self, text="Sort Ascending",
            bg="white", fg="#4b1f24", width=20, pady=10, cursor="hand2",
            command=lambda: self.sort_order(False)
        ).pack(pady=5)

        tk.Button(
            self, text="Sort Descending",
            bg="white", fg="#4b1f24", width=20, pady=10, cursor="hand2",
            command=lambda: self.sort_order(True)
        ).pack(pady=5)

        tk.Button(
            self, text="Back to Menu",
            bg="white", fg="#4b1f24", cursor="hand2",
            command=lambda: controller.show_frame("MenuPage")
        ).pack(pady=20)

    def sort_order(self, reverse):
        # List is sorted using Python's sort(). Reverse is pretty much "true" which means to arrange in descending order
        self.controller.students.sort(key=lambda s: s["percentage"], reverse=reverse)
        save_student_data(self.controller.students)
        messagebox.showinfo("Sorted", "Student records sorted successfully!")
        self.controller.show_frame("AllStudentsPage")


# RUN APP
if __name__ == "__main__":
    students = load_student_data()
    if students:
        app = StudentApp(students)
        app.mainloop()