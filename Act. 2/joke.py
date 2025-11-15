import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import pygame

# LOAD JOKES
def load_jokes():
    # This load the jokes from my "radomJokes.txt" in my resources folder.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    jokes_path = os.path.join(base_dir, "resources", "randomJokes.txt") # File directory

    jokes = []
    with open(jokes_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "?" not in line: # Skips invalid lines
                continue
            setup, punchline = line.split("?", 1)
            jokes.append((setup.strip() + "?", punchline.strip()))
    return jokes

# CHAT BUBBLE
def add_chat_bubble(frame, text, sender="alexa"):
    # Creates the "messenger" feel of the app (theme)
    # Determine bubble color and alignment
    if sender == "you":
        bubble_color = "#DCF8C6"  # user green
        side = "right"  # align to right
        anchor_val = "e"
        padx_val = (50, 5)  # adds more space to the left
    else:
        bubble_color = "#FFFFFF"  # bot white
        side = "left"  # align to left
        anchor_val = "w"
        padx_val = (5, 50)  # adds more space to the right

    # Bubble frame
    bubble = tk.Frame(
        frame,
        bg=bubble_color,
        padx=10, pady=7,
        bd=1, relief="solid"
    )
    bubble.pack(anchor=anchor_val, pady=5, padx=padx_val)

    # Label inside bubble
    label = tk.Label(
        bubble,
        text=text,
        font=("Arial", 12),
        wraplength=260, # to wrap text
        justify="left",
        bg=bubble_color
    )
    label.pack()


# MAIN APP CLASS
class alexaJoke:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa, Tell Me A Joke")
        self.root.geometry("360x640")
        self.root.resizable(False, False) # disables resizing (same as Act. 1)

        self.jokes = load_jokes()
        self.current_setup = ""
        self.current_punchline = ""

        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_image = ImageTk.PhotoImage(file=os.path.join(base_dir, "resources", "icon.jpg"))
        root.iconphoto(False, icon_image)

        # START SCREEN BG IMAGE
        self.start_bg_img = ImageTk.PhotoImage(
            Image.open(os.path.join(base_dir, "resources", "start.png")).resize((360, 640))
        )

        # START SCREEN
        self.start_frame = tk.Frame(root)
        self.start_frame.pack(fill="both", expand=True)

        # to add bg image
        self.start_bg_label = tk.Label(self.start_frame, image=self.start_bg_img)
        self.start_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # the start button to begin app
        start_btn = tk.Button(self.start_frame, text="Start", font=("Comic Sans MS", 14), width=15,
                            command=self.open_chat)
        start_btn.place(relx=0.5, rely=0.65, anchor="center") 

        # exit or quit button to leave app
        quit_btn = tk.Button(self.start_frame, text="Quit", font=("Comic Sans MS", 14), width=15,
                            command=root.destroy, bg="tomato", fg="white")
        quit_btn.place(relx=0.5, rely=0.74, anchor="center") 

        # CHAT SCREEN
        self.chat_frame = tk.Frame(root, bg="#5FB1EF")

        # Canvas + scrollbar container
        self.chat_area_frame = tk.Frame(self.chat_frame, bg="#5FB1EF")
        self.chat_area_frame.pack(fill="both", expand=True)

        self.chat_canvas = tk.Canvas(self.chat_area_frame, bg="#5FB1EF", highlightthickness=0)
        self.chat_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_area_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_inner_frame = tk.Frame(self.chat_canvas, bg="#5FB1EF")
        self.chat_canvas.create_window((0, 0), window=self.chat_inner_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_inner_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )

        # Bottom buttons frame
        self.bottom_frame = tk.Frame(self.chat_frame, bg="#fff")
        self.bottom_frame.pack(side="bottom", fill="x")

        self.ask_btn = tk.Button(self.bottom_frame, text="Alexa tell me a Joke",
                                font=("Comic Sans MS", 12), width=20, bg="#DCF8C6",
                                command=self.tell_joke)
        self.ask_btn.pack(pady=5)

        self.punch_btn = tk.Button(self.bottom_frame, text="Show Punchline",
                                font=("Comic Sans MS", 12), width=20,
                                state="disabled", bg="pink",
                                command=self.show_punchline)
        self.punch_btn.pack(pady=5)

        # BACKGROUND MUSIC
        pygame.mixer.init()
        music_path = os.path.join(base_dir, "resources", "goofy.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1) # loops the music throughout the game

    # CHAT OPENING
    def open_chat(self):
        # changes screen from start to main chat (joke)
        self.start_frame.pack_forget()
        self.chat_frame.pack(fill="both", expand=True)
        add_chat_bubble(self.chat_inner_frame, "What's up? Wanna activate your funny bone? Tap 'Alexa tell me a Joke' to start C:", sender="alexa")
        self.auto_scroll() # scrolls to the bottom automatically

    # JOKE FUNCTIONS
    def tell_joke(self):
        # selects random joke
        self.current_setup, self.current_punchline = random.choice(self.jokes)
        add_chat_bubble(self.chat_inner_frame, "Hey, Alexa.. Tell me a joke!", sender="you")
        add_chat_bubble(self.chat_inner_frame, self.current_setup, sender="alexa")
        self.punch_btn.config(state="normal") # enables the punchline button
        self.auto_scroll()

    def show_punchline(self):
        # Add punchline to chat
        add_chat_bubble(self.chat_inner_frame, self.current_punchline, sender="alexa")
        self.punch_btn.config(state="disabled")
        self.auto_scroll()

        # Play clown honk sound for comedic effect
        base_dir = os.path.dirname(os.path.abspath(__file__))
        joke_path = os.path.join(base_dir, "resources", "joke.mp3")  # your laugh sound file
        if os.path.exists(joke_path):
            try:
                # Initialize mixer if not already
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                laugh_sound = pygame.mixer.Sound(joke_path)
                laugh_sound.set_volume(0.3)  # adjust volume
                laugh_sound.play()
            except Exception as e:
                print("Error playing laugh sound:", e)


    # AUTO SCROLL
    def auto_scroll(self):
        # allows automatic scrolling to show latest message
        self.root.after(50, lambda: self.chat_canvas.yview_moveto(1.0))

# RUN PROGRAM
root = tk.Tk()
app = alexaJoke(root)

root.mainloop()
