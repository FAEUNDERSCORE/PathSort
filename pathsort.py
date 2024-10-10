import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class PathSort:
    def __init__(self):
        self.root = tk.Tk()
        self.files = 0
        self.root.title("PathSort")

        self.root.resizable(False, False)

        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        icon_path = os.path.join(application_path, "icon.ico")
        self.root.iconbitmap(icon_path)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.update_idletasks()

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 16), padding=10)
        self.style.configure("TButton", font=("Arial", 14), padding=10)

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="This tool sorts files in a directory by their extension.", wraplength=self.root.winfo_width(), justify="center")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.directory_path = ""

        self.button = ttk.Button(self.root, text="Select Directory", command=self.select_directory)
        self.button.grid(row=1, column=0, padx=10, pady=10)

        self.label2 = ttk.Label(self.root, text="Selected directory : None", wraplength=self.root.winfo_width(), justify="center", foreground="red")
        self.label2.grid(row=2, column=0, padx=10, pady=10)

        self.sort_button = ttk.Button(self.root, text="Sort", command=lambda: self.pathsort(self.directory_path), state=tk.DISABLED)
        self.sort_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        if not self.directory_path:
            return
        self.label2.config(text="Selected directory : " + self.directory_path, foreground="green")
        self.sort_button.config(state=tk.NORMAL)
    
    def pathsort(self, path):
        try:
            for filename in os.listdir(path):
                if filename.lower().startswith("pathsort"):
                    continue
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    extension = filename.split(".")[-1].upper()
                    folder = os.path.join(path, extension)
                    os.makedirs(folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(folder, filename))
                    self.files += 1
            messagebox.showinfo("Confirmation", f"Sorted {self.files} files.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.clear()
        
    def clear(self):
        self.directory_path = ""
        self.label2.config(text="Selected directory : None", foreground="red")
        self.sort_button.config(state=tk.DISABLED)
        self.files = 0

    def run(self):
        self.root.mainloop()
    
    def on_closing(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()
        label = ttk.Label(self.root, text="See you later unorganized files!", wraplength=self.root.winfo_width(), justify="center")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.root.after(1000, self.root.destroy)

if __name__ == "__main__":
    app = PathSort()
    app.run()