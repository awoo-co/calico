# output.py
# This file contains the core logic for creating the .calico file.
# It is separated from the GUI for better organization.

import os
import zipfile

def create_calico_file(file_list, output_filename, output_dir):
    """
    Creates a .calico file from a list of files and saves it to a specified directory.

    Args:
        file_list (list): A list of strings, where each string is the path to a file to be added.
        output_filename (str): The desired name for the output .calico file.
        output_dir (str): The directory where the file will be saved.

    Returns:
        tuple: A tuple containing a boolean (success) and a message string.
    """
    # Ensure the output filename has the .calico extension
    if not output_filename.endswith(".calico"):
        output_filename += ".calico"
    
    # Construct the full path for the output file
    output_path = os.path.join(output_dir, output_filename)
    
    # Use a temporary .zip filename for creation to avoid issues with the final name
    temp_zip_filename = output_path.replace(".calico", ".zip")

    try:
        # Check if the number of files exceeds the limit of 20
        if len(file_list) > 20:
            return False, "The maximum number of files is 20. Please reduce the number of files."

        # Create the zip archive with the temporary name
        with zipfile.ZipFile(temp_zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_list:
                # Check if the file exists before adding it
                if os.path.exists(file_path):
                    # Add the file to the zip archive, preserving its base name
                    zipf.write(file_path, os.path.basename(file_path))
                    print(f"Successfully added: {os.path.basename(file_path)}")
                else:
                    print(f"Warning: File not found - {file_path}. It was skipped.")
        
        # Rename the temporary .zip file to the final .calico file
        os.rename(temp_zip_filename, output_path)
        return True, f"Successfully created {output_filename} containing {len(file_list)} files in the '{output_dir}' folder."

    except Exception as e:
        # Clean up the temporary file if an error occurred
        if os.path.exists(temp_zip_filename):
            os.remove(temp_zip_filename)
        return False, f"An error occurred: {e}"
