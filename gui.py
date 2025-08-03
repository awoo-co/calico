# gui.py
# This file contains the CalicoCreatorApp class, which handles all
# the Tkinter GUI components and user interactions.

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from output import create_calico_file

class CalicoCreatorApp(tk.Tk):
    """
    A simple GUI application to create a .calico file from a list of files.
    """
    def __init__(self, output_folder_path):
        super().__init__()
        self.title("Calico File Creator")
        self.geometry("600x450")  # Resized the window to be taller
        
        self.output_folder_path = output_folder_path
        self.files_to_add = []
        
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and lays out the GUI widgets.
        """
        # --- Frame for file list and buttons ---
        files_frame = tk.Frame(self, padx=10, pady=10)
        files_frame.pack(fill="both", expand=True)
        
        files_label = tk.Label(files_frame, text="Files to be added (max 20):")
        files_label.pack(anchor="w")

        self.listbox = tk.Listbox(files_frame, selectmode=tk.MULTIPLE, height=10)
        self.listbox.pack(fill="both", expand=True, pady=5)

        button_frame = tk.Frame(files_frame)
        button_frame.pack(fill="x", pady=5)
        
        add_button = tk.Button(button_frame, text="Add Files", command=self.add_files)
        add_button.pack(side="left", padx=5)
        
        remove_button = tk.Button(button_frame, text="Remove Selected", command=self.remove_files)
        remove_button.pack(side="left", padx=5)

        # --- Frame for output filename and creation button ---
        output_frame = tk.Frame(self, padx=10, pady=10)
        output_frame.pack(fill="x")

        output_label = tk.Label(output_frame, text="Output .calico file name:")
        output_label.pack(anchor="w")

        self.output_entry = tk.Entry(output_frame, width=50)
        self.output_entry.pack(fill="x", pady=5)
        self.output_entry.insert(0, "my_archive.calico")

        create_button = tk.Button(output_frame, text="Create .calico File", command=self.handle_create_file)
        create_button.pack(pady=10)

    def add_files(self):
        """
        Opens a file dialog to select files and adds them to the listbox.
        """
        selected_files = filedialog.askopenfilenames(
            title="Select files to add",
            filetypes=[("All files", "*.*")]
        )
        
        for file_path in selected_files:
            if len(self.files_to_add) < 20:
                if file_path not in self.files_to_add:
                    self.files_to_add.append(file_path)
                    self.listbox.insert(tk.END, os.path.basename(file_path))
            else:
                messagebox.showwarning("File Limit Exceeded", "You can only add up to 20 files.")
                break

    def remove_files(self):
        """
        Removes the selected files from the listbox and the internal list.
        """
        selected_indices = self.listbox.curselection()
        
        for index in reversed(selected_indices):
            removed_file_path = self.files_to_add.pop(index)
            self.listbox.delete(index)

    def handle_create_file(self):
        """
        Handles the file creation process by calling the function in output.py.
        """
        output_filename = self.output_entry.get()
        if not output_filename:
            messagebox.showerror("Error", "Please enter a name for the output file.")
            return

        if not self.files_to_add:
            messagebox.showerror("Error", "Please add at least one file.")
            return

        # Call the file creation function from output.py
        result, message = create_calico_file(self.files_to_add, output_filename, self.output_folder_path)

        if result:
            messagebox.showinfo("Success!", message)
            # Clear the listbox and the internal list on success
            self.files_to_add = []
            self.listbox.delete(0, tk.END)
        else:
            messagebox.showerror("Error", message)
