import tkinter as tk
from tkinter import font, messagebox
import random # to randomize questions and operations
import pygame # Info gathered from GeeksforGeeks
from PIL import Image, ImageTk # for images
import os

pygame.mixer.init() # Applied to allow sounds/music

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where this script lives

# Background music
pygame.mixer.music.load(os.path.join(BASE_DIR, "bg.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # loop indefinitely

correct_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "correct.wav")) # Correct answer sound effect
wrong_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "wrong.wav")) # Wrong answer sound effect

root = tk.Tk()
root.title("Arithmetic Quiz Game")
root.geometry("800x500")
root.resizable(False, False) # Disables full screen option

icon_image = ImageTk.PhotoImage(file=os.path.join(BASE_DIR, "icon.jpg"))
root.iconphoto(False, icon_image) # Icon photo for my pages (Same icons for each page)

# Background images designed by me
menu_bg_photo = ImageTk.PhotoImage(
    Image.open(os.path.join(BASE_DIR, "menu.png")).resize((800, 500), Image.LANCZOS) # Background image for the menu page
)
instruction_bg_photo = ImageTk.PhotoImage(
    Image.open(os.path.join(BASE_DIR, "ins.png")).resize((800, 500), Image.LANCZOS) # Background image for the instructions page
)
difficulty_bg_photo = ImageTk.PhotoImage(
    Image.open(os.path.join(BASE_DIR, "dif.png")).resize((800, 500), Image.LANCZOS) # Background image for the select difficulty page
)
quiz_bg_photo = ImageTk.PhotoImage(
    Image.open(os.path.join(BASE_DIR, "quiz.png")).resize((800, 500), Image.LANCZOS) # Background image for the quiz page
)
hight_bg_photo = ImageTk.PhotoImage(
    Image.open(os.path.join(BASE_DIR, "high.png")).resize((800, 500), Image.LANCZOS) # Background image if user gets high score
)
med_bg_photo = ImageTk.PhotoImage(
    Image.open(os.path.join(BASE_DIR, "med.png")).resize((800, 500), Image.LANCZOS) # Background image if user gets average score
)
low_bg_photo = ImageTk.PhotoImage(
    Image.open(os.path.join(BASE_DIR, "low.png")).resize((800, 500), Image.LANCZOS) # Background image if user gets low/fail score
)

# FUNCTIONS

def resetScreen():
    for widget in root.winfo_children():
        widget.destroy()

def displayMenu():
    resetScreen() # Removes other widgets
    bg_label = tk.Label(root, image=menu_bg_photo) # Bg image for menu page
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    start_btn = tk.Button(root, text="Start Game", command=instructionPage,
                        width=20, height=2, font=("Arial", 12, "bold"), bg="lightblue") # Start game button
    start_btn.place(relx=0.5, rely=0.65, anchor="center")  # Y axis adjusted to desired position

    quit_btn = tk.Button(root, text="Quit Game", command=on_exit, 
                        width=20, height=2, font=("Arial", 12, "bold"), bg="tomato", fg="white") # Quit Game button
    quit_btn.place(relx=0.5, rely=0.8, anchor="center")

def instructionPage(): # This page shows the instructions of the game
    resetScreen()
    bg_label = tk.Label(root, image=instruction_bg_photo) # Bg image for instructions page
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    button_frame = tk.Frame(root, bg="")  # transparent frame
    button_frame.place(relx=0.5, rely=0.78, anchor="center")

    continue_btn = tk.Button(button_frame, text="Continue", command=selectDifficulty,
                            width=20, height=2, bg="lightblue", font=("Arial", 12, "bold"),
                            relief="flat", borderwidth=0, highlightthickness=0) # Continue button to move to the next page
    continue_btn.pack(side="left", padx=20)

    back_btn = tk.Button(button_frame, text="Back to Menu", command=displayMenu,
                        width=20, height=2, bg="lightgray", font=("Arial", 12, "bold"),
                        relief="flat", borderwidth=0, highlightthickness=0) # Back to Menu button
    back_btn.pack(side="left", padx=20)
    
def play_quiz(select_diff):
    global currentProblem, level, marks # Starts the quiz after selecting difficulty
    currentProblem = 1 # Question counter
    level = select_diff
    marks = 0 # Score at the beginning of the game
    displayProblem()

def selectDifficulty(): # User shall select the difficulty level
    resetScreen()
    bg_label = tk.Label(root, image=difficulty_bg_photo) # Bg image for difficulty selection page
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    easy_btn = tk.Button(root, text="Easy (1-digit)", width=20, height=2, command=lambda: play_quiz("easy"),
            bg="DarkOliveGreen1", font=("Helvetica", 12, "bold")) # Easy level button
    easy_btn.place(relx=0.5, rely=0.39, anchor="center") 
    
    moderate_btn = tk.Button(root, text="Moderate (2-digit)", width=20, height=2, command=lambda: play_quiz("moderate"),
            bg="light goldenrod", font=("Helvetica", 12, "bold")) # Moderate level button
    moderate_btn.place(relx=0.5, rely=0.53, anchor="center") 
        
    advanced_btn = tk.Button(root, text="Advanced (4-digit)", width=20, height=2, command=lambda: play_quiz("advanced"),
            bg="salmon", font=("Helvetica", 12, "bold")) # Advanced level button
    advanced_btn.place(relx=0.5, rely=0.67, anchor="center")  

    back_btn = tk.Button(root, text="Back", command=instructionPage, width=20, height=2,
            bg="lightgray", font=("Helvetica", 12, "bold")) # Back button to return to the instructions page
    back_btn.place(relx=0.5, rely=0.81, anchor="center")

def randomInt(select_diff): 
    if select_diff == "easy":
        return random.randint(1, 9), random.randint(1, 9) # Generates 1 digit random numbers
    elif select_diff == "moderate":
        return random.randint(10, 99), random.randint(10, 99) # Generates 2 digit random numbers
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999) # Generates 4 digit random numbers

def decideOperation(): # Randomizes operation for the quiz
    return random.choice(['+', '-'])

def displayProblem(): # Displays the question
    global num1, num2, operation, user_attempts

    resetScreen()
    bg_label = tk.Label(root, image=quiz_bg_photo) # Bg image for quiz page
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    num1, num2 = randomInt(level) # Create random question
    operation = decideOperation()
    user_attempts = 2 # Attempts given to the user

    question_lbl = tk.Label(root, text=f"Question {currentProblem}/10", font=("Comic Sans Ms", 25), bg="#32651b", fg="white")
    question_lbl.place(relx=0.5, rely=0.37, anchor="center") 
    
    operator_lbl = tk.Label(root, text=f"{num1} {operation} {num2} =", font=("Comic Sans Ms", 25), bg="#3c6d28", fg="white")
    operator_lbl.place(relx=0.5, rely=0.49, anchor="center") 

    global ans_entry # Boxes for users to enter their answer
    ans_entry = tk.Entry(root, font=("Comic Sans Ms", 16), justify='center')
    ans_entry.place(relx=0.5, rely=0.58, anchor="center") 
    ans_entry.focus()

    sub_btn = tk.Button(root, text="Submit", command=verifyAnswer, width=15, bg="lightblue", font=("Helvetica", 13, "bold")) # Submit button
    sub_btn.place(relx=0.5, rely=0.67, anchor="center") 

    attempt_lbl = tk.Label(root, text=f"Attempts left: {user_attempts}", name="attempt_label", bg="darkred", fg="white",
            font=("Helvetica", 10, "bold")) # Label to let user know how many attempts they have left in a problem
    attempt_lbl.place(relx=0.5, rely=0.75, anchor="center") 

def ansCorrect(input_ans):
    try: # Checks if user's answer is correct
        correct_answer = eval(f"{num1} {operation} {num2}")
        return int(input_ans) == correct_answer
    except ValueError:
        return False

def verifyAnswer():
    global marks, currentProblem, user_attempts # To verify the answer and to update score

    input_ans = ans_entry.get()

    if ansCorrect(input_ans):
        correct_sound.play() # Sound will play if the answer is correct
        if user_attempts == 2: 
            marks += 10 # Score if first try answer is correct
            messagebox.showinfo("Amazing!", "Correct on first try 🏆! (+10 points)")
        else:
            marks += 5 # User's second try and the score achieved if correct
            messagebox.showinfo("Alright!", "Correct on second try 🏅! (+5 points)")
        nextProblem()
    else:
        wrong_sound.play() # Sound will play if answer is wrong
        user_attempts -= 1
        if user_attempts > 0:
            messagebox.showwarning("Warning", f"Wrong answer 😔. Try again! ({user_attempts} attempt left)")
            root.nametowidget(".attempt_label").config(text=f"Attempts left: {user_attempts}") # This label shows how many attempts left
        else:
            messagebox.showerror("Fail Attempt", "No attempts left for this question 💔.")
            nextProblem()

def nextProblem():
    global currentProblem # To proceed to the next question or to the result page once quiz is complete
    currentProblem += 1
    if currentProblem <= 10:
        displayProblem()
    else:
        displayResults() # After quiz is over, user is moved to result page

def displayResults():
    resetScreen() # Decide which background to use based on score
    if marks >= 70:
        bg_label = tk.Label(root, image=hight_bg_photo)
    elif marks >= 50:
        bg_label = tk.Label(root, image=med_bg_photo)
    else:
        bg_label = tk.Label(root, image=low_bg_photo)

    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    result_lbl = tk.Label(root, text=f"Final Score: {marks}/100", font=("Comic Sans MS", 20, "bold"),
            bg="#32651b", fg="white") # Show final score
    result_lbl.place(relx=0.5, rely=0.47, anchor="center") 

    if marks >= 90: # Determine grade result depending on the score
        grade = "A+"
    elif marks >= 80:
        grade = "A"
    elif marks >= 70:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    elif marks >= 50:
        grade = "D"
    else:
        grade = "F"

    grade_lbl = tk.Label(root, text=f"Your Grade: {grade}",
            font=("Comic Sans MS", 18, "bold"), bg="#32651b", fg="white")
    grade_lbl.place(relx=0.5, rely=0.56, anchor="center") 
    
    # Buttons to give user option either to play again or leave the game
    restart_btn = tk.Button(root, text="Play Again", command=displayMenu,
            width=20, bg="lightblue", font=("Helvetica", 12, "bold"))
    restart_btn.place(relx=0.5, rely=0.67, anchor="center") 

    exit_btn = tk.Button(root, text="Exit Game", command=on_exit,
            width=20, bg="tomato", fg="white", font=("Helvetica", 12, "bold"))
    exit_btn.place(relx=0.5, rely=0.77, anchor="center") 

def on_exit(): # Game stops as soon as player leaves the game
    pygame.mixer.music.stop() # Music stops upon exiting
    root.destroy()

# Starts the game at the menu page
displayMenu() 


root.mainloop()

