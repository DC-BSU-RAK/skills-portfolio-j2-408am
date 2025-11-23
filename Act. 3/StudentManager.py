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
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

# LOAD STUDENT DATA
def load_student_data(filename=None):
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

# MAIN APP
class StudentApp(tk.Tk):
    def __init__(self, students):
        super().__init__()
        self.title("Student Management System")
        self.geometry("724x650")
        self.resizable(False, False)
        self.students = students # To store the student data
        
        # School icon for the app
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_image = ImageTk.PhotoImage(file=os.path.join(base_dir, "assets", "icon.png"))
        self.iconphoto(False, icon_image)

        # Frame container
        self.container = tk.Frame(self, bg="#4b1f24")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MenuPage, AllStudentsPage, SelectStudentPage, StudentDetailPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        # Makes sure the menu page is shown first
        self.show_frame("MenuPage")

    # To switch to different pages
    def show_frame(self, name):
        self.frames[name].tkraise()

# MENU PAGE
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        script_dir = os.path.dirname(os.path.abspath(__file__))
        # All pages contain the same header image for uniformity
        header_path = os.path.join(script_dir, "assets", "header.png")
        header_img = Image.open(header_path).resize((724, 200), Image.Resampling.LANCZOS)
        self.header_photo = ImageTk.PhotoImage(header_img)
        tk.Label(self, image=self.header_photo, bg="#4b1f24").pack(fill="x")

        tk.Label(self, text="Student Management Menu",
                font=("Georgia", 26, "bold"), fg="white", bg="#4b1f24").pack(pady=25)

        btn_frame = tk.Frame(self, bg="#4b1f24")
        btn_frame.pack(pady=10)

        # To create the buttons for the menu page
        def create_button(text, cmd):
            btn = tk.Button(btn_frame, text=text, command=cmd, font=("Georgia", 12),
                            bg="white", fg="#4b1f24", width=35, pady=10, relief="flat", bd=0, cursor="hand2")
            btn.pack(pady=10)
            return btn

        create_button("View All Student Records",
                    lambda: controller.show_frame("AllStudentsPage"))
        create_button("View Individual Student Record",
                    lambda: controller.show_frame("SelectStudentPage"))
        create_button("Show Student with Highest Overall Mark", self.show_highest)
        create_button("Show Student with Lowest Overall Mark", self.show_lowest)

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
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        # Header image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        header_path = os.path.join(script_dir, "assets", "header.png")
        header_img = Image.open(header_path).resize((724, 200), Image.Resampling.LANCZOS)
        self.header_photo = ImageTk.PhotoImage(header_img)
        tk.Label(self, image=self.header_photo, bg="#4b1f24").pack(fill="x")

        tk.Label(self, text="All Student Records",
                font=("Georgia", 22, "bold"), bg="#4b1f24", fg="white").pack(pady=10)

    # Table columns to show complete info to user
        columns = ("Student ID", "Name", "Coursework Total", "Exam Score", "Overall Percentage", "Grade")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(pady=10)

        # Button to let user return to the menu/previous page
        tk.Button(self, text="Back to Menu", width=20, cursor="hand2", bg="white", fg="#4b1f24",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=10)

    # To update table every time page is shown
    def tkraise(self, *args, **kwargs):
        self.tree.delete(*self.tree.get_children()) # Clears old data
        grade_colors = {'A':'#a8e6cf','B':'#dcedc1','C':'#fff9b0','D':'#ffd3b6','F':'#ff8b94'}
        for i, s in enumerate(self.controller.students):
            self.tree.insert("", tk.END, values=(
                s['id'], s['name'], s['coursework_total'], s['exam'],
                f"{s['percentage']:.2f}%", s['grade']
            ))
            # Color-coded row based on the student's grade for organizational purposes
            item = self.tree.get_children()[-1]
            self.tree.tag_configure(f"grade{i}", background=grade_colors.get(s['grade'], "white"))
            self.tree.item(item, tags=(f"grade{i}",))
        super().tkraise(*args, **kwargs)

# SELECT STUDENT PAGE
class SelectStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        script_dir = os.path.dirname(os.path.abspath(__file__))
        header_path = os.path.join(script_dir, "assets", "header.png")
        header_img = Image.open(header_path).resize((724, 200), Image.Resampling.LANCZOS)
        self.header_photo = ImageTk.PhotoImage(header_img)
        tk.Label(self, image=self.header_photo, bg="#4b1f24").pack(fill="x")

        tk.Label(self, text="Select a Student",
                font=("Georgia", 22, "bold"), bg="#4b1f24", fg="white").pack(pady=10)

        # Contains a list of students with their ID number
        self.listbox = tk.Listbox(self, width=50, height=10)
        self.listbox.pack(pady=10)

        # Buttons to proceed or return to the page
        tk.Button(self, text="View Student Record", cursor="hand2", bg="white", fg="#4b1f24", command=self.view_student).pack(pady=5)
        tk.Button(self, text="Back to Menu", cursor="hand2", bg="white", fg="#4b1f24",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=5)

    def tkraise(self, *args, **kwargs):
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
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#4b1f24")
        self.controller = controller

        script_dir = os.path.dirname(os.path.abspath(__file__))
        header_path = os.path.join(script_dir, "assets", "header.png")
        header_img = Image.open(header_path).resize((724, 200), Image.Resampling.LANCZOS)
        self.header_photo = ImageTk.PhotoImage(header_img)
        tk.Label(self, image=self.header_photo, bg="#4b1f24").pack(fill="x")

        tk.Label(self, text="Student Record",
                font=("Georgia", 22, "bold"), bg="#4b1f24", fg="white").pack(pady=10)

        cols = ("Attribute", "Value")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=6)
        self.tree.heading("Attribute", text="Attribute")
        self.tree.heading("Value", text="Value")
        self.tree.column("Attribute", width=150, anchor="center")
        self.tree.column("Value", width=200, anchor="center")
        self.tree.pack(pady=20)

        tk.Button(self, text="Back to Menu", cursor="hand2", bg="white", fg="#4b1f24",
                command=lambda: controller.show_frame("MenuPage")).pack(pady=10)

    # Display data for chosen student (single)
    def set_student(self, s):
        self.tree.delete(*self.tree.get_children())
        grade_colors = {'A':'#a8e6cf','B':'#dcedc1','C':'#fff9b0','D':'#ffd3b6','F':'#ff8b94'}
        data = [
            ("Name", s['name']),
            ("Student ID", s['id']),
            ("Coursework Total", s['coursework_total']),
            ("Exam Mark", s['exam']),
            ("Overall Percentage", f"{s['percentage']:.2f}%"),
            ("Grade", s['grade']),
        ]
        for attr, value in data:
            self.tree.insert("", tk.END, values=(attr, value))
            # Grade row will only be colored to highlight the final grade
            if attr == "Grade":
                item = self.tree.get_children()[-1]
                self.tree.tag_configure("grade", background=grade_colors.get(value, "white"))
                self.tree.item(item, tags=("grade",))

# RUN APP
if __name__ == "__main__":
    students = load_student_data()
    if students:
        app = StudentApp(students)
        app.mainloop()