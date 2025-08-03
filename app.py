# app.py
# This is the main entry point for the Calico Creator application.
# It sets up the environment and launches the GUI.

import os
from gui import CalicoCreatorApp

def create_output_directory():
    """
    Creates a dedicated 'output' directory if it doesn't already exist.
    All created .calico files will be stored here.
    """
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    return output_dir

if __name__ == "__main__":
    # Create the output directory at startup
    output_folder_path = create_output_directory()

    # Create and run the GUI application
    app = CalicoCreatorApp(output_folder_path)
    app.mainloop()
