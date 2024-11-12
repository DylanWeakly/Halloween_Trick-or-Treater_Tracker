# Program Author: Dylan Weakly
# Program Date: 10/26/2024
# Program Purpose: To track the amount of people who come trick or treating on Halloween
import tkinter as tk
from PIL import Image, ImageTk
import sqlite3

class ToTAccumulator:
    def __init__(self, gui):
        self.conn = sqlite3.connect("halloween_tracker.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS counter (
                id INTEGER PRIMARY KEY,
                num_of_people INTEGER NOT NULL
                )
            """)
        self.conn.commit()

        self.root = gui
        self.root.title("Halloween Trick-or-Treat Counter")

        self.accumulator = 0

        self.background_image = Image.open("halloween_freepik.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(gui, width=self.background_photo.width(), height=self.background_photo.height())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.label = tk.Label(
            gui,
            text="There have been\nno trick-or-treaters yet.",
            font=('Helvetica', 36),
            fg='white',
            bg='black')
        self.label_window = self.canvas.create_window(490, 170, anchor="nw", window=self.label)

        self.add_button = tk.Button(
            gui,
            text="   Add 1   ",
            command=self.increment_accumulator,
            font=('Helvetica', 24),
            fg='orange',
            bg='black')
        self.add_button_window = self.canvas.create_window(535, 500, anchor="nw", window=self.add_button)

        self.reset_button = tk.Button(
            gui,
            text="Reset Counter",
            command=self.reset_accumulator,
            font=('Helvetica', 18),
            fg='orange',
            bg='black')
        self.reset_button_window = self.canvas.create_window(630, 650, anchor="nw", window=self.reset_button)

        self.minus1_button = tk.Button(
            gui,
            text="Subtract 1",
            command=self.subtract_one,
            font=('Helvetica', 24),
            fg='orange',
            bg='black')
        self.minus1_window = self.canvas.create_window(720, 500, anchor="nw", window=self.minus1_button)

        self.save_button = tk.Button(
            gui,
            text="Save Data",
            command=self.store_accumulator,
            font=('Helvetica', 24),
            fg='orange',
            bg='black')
        self.save_button.window = self.canvas.create_window(720, 570, anchor="nw", window=self.save_button)

        self.load_button = tk.Button(
            gui,
            text="Load Data",
            command=self.load_accumulator,
            font=('Helvetica', 24),
            fg='orange',
            bg='black')
        self.load_button_window = self.canvas.create_window(530, 570, anchor="nw", window=self.load_button)

    def increment_accumulator(self):
        self.accumulator += 1
        self.update_label()

    def reset_accumulator(self):
        self.accumulator = 0
        self.update_label()

    def subtract_one(self):
        if self.accumulator > 0:
            self.accumulator -= 1
        self.update_label()

    def update_label(self):
        if self.accumulator == 1:
            self.label.configure(text=f"There has been\n{self.accumulator}\ntrick-or-treater tonight.")
        elif self.accumulator == 0:
            self.label.configure(text="There have been\nno trick-or-treaters yet.")
        else:
            self.label.configure(text=f"There have been\n{self.accumulator}\ntrick-or-treaters tonight.")

    def load_accumulator(self):
        # Load the most recent count from the database
        self.cursor.execute("SELECT num_of_people FROM counter ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            self.accumulator = result[0]
            self.update_label()
        else:
            self.label.configure(text="No saved count found.")

    def store_accumulator(self):
        # Store the current accumulator value in the database
        self.cursor.execute("INSERT OR REPLACE INTO counter (id, num_of_people) VALUES (2024, ?)", (self.accumulator,))
        self.conn.commit()
        self.label.configure(text="Count stored in database!")

    def __del__(self):
        # Close the database connection when the instance is deleted
        self.conn.close()

if __name__ == '__main__':
    thisGUI = tk.Tk()
    thisGUI.geometry("1400x800+12+0")
    theApp = ToTAccumulator(thisGUI)
    thisGUI.mainloop()
