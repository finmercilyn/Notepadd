import tkinter as tk
from tkinter import font, colorchooser, scrolledtext, filedialog
from datetime import datetime
import sys
import os

class Notepadd:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepadd")
        self.root.geometry("1000x700")
        self.file_path = None

        self.my_font_family = tk.StringVar(value="Arial")
        self.my_font_size = tk.IntVar(value=14)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="New", command=self.new_file)
        edit_menu.add_command(label="Save", command=self.save_file)

        top_frame = tk.Frame(root, height=40)
        top_frame.pack(side="top", fill="x")

        tk.Label(top_frame, text="Font").pack(side="left", padx=5)
        tk.Entry(top_frame, textvariable=self.my_font_family, width=12).pack(side="left")
        tk.Label(top_frame, text="Size").pack(side="left", padx=5)
        tk.Entry(top_frame, textvariable=self.my_font_size, width=4).pack(side="left")
        tk.Button(top_frame, text="Apply", command=self.apply_font).pack(side="left", padx=5)

        tk.Button(top_frame, text="Text Color", command=self.change_color).pack(side="left", padx=5)
        tk.Button(top_frame, text="BG Color", command=self.change_bg).pack(side="left", padx=5)

        self.text_area = scrolledtext.ScrolledText(root, wrap="word", font=("Arial", 14))
        self.text_area.pack(expand=True, fill="both")

        if len(sys.argv) > 1:
            self.open_from_arg(sys.argv[1])
        else:
            self.insert_datetime()

    def insert_datetime(self):
        now = datetime.now().strftime("%A, %b %d, %Y at %I:%M %p")
        self.text_area.insert("1.0", now + "\n\n")

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.file_path = None
        self.insert_datetime()

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")]
            )
        if self.file_path:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get("1.0", tk.END))

    def open_from_arg(self, path):
        if os.path.exists(path):
            self.file_path = path
            with open(path, "r", encoding="utf-8") as f:
                self.text_area.insert("1.0", f.read())

    def apply_font(self):
        f = font.Font(
            family=self.my_font_family.get(),
            size=self.my_font_size.get()
        )
        self.text_area.configure(font=f)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.configure(fg=color)

    def change_bg(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.configure(bg=color)

root = tk.Tk()
app = Notepadd(root)
root.mainloop()