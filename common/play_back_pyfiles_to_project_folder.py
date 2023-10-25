"""
Overview:
This script performs two main tasks:
1. It reads an input text file that contains the code of multiple Python files. It replaces the
   original project folder name with an alternate one and writes the modified lines to an output text file.
2. It then asynchronously reads the output text file, extracts the code for each Python file, and writes it
   back to its respective original file, potentially in a new directory.

The script is designed to be run as a standalone program and uses Python's asyncio for asynchronous file operations.

Author: Joe Zhu
Date: Oct 25, 2023
"""

import asyncio
import aiofiles
import os
from datetime import datetime

def set_project_root_directory(inputf, outf, project_folder_name, alternate_project_folder_name):
    """
    Read the input file and replace the original project folder name with an alternate one.
    
    Parameters:
    - inputf (str): Path to the input file
    - outf (str): Path to the output file
    - project_folder_name (str): Original project folder name to find
    - alternate_project_folder_name (str): New project folder name to replace with
    
    Returns:
    - bool: True if the file path is valid, otherwise False
    """
    file_path_valid = False
    with open(inputf, 'r') as f:
        lines = f.readlines()

    # Replace original project folder name with the alternate one
    for idx, line in enumerate(lines):
        if 'File: C' in line or '# End of' in line:
            line = line.replace('\\', '/') 
            if project_folder_name in line:
                lines[idx] = line.replace(project_folder_name, alternate_project_folder_name)
                file_path_valid = True

    # Write the updated lines to the output file
    with open(outf, 'w') as f:
        f.write(''.join(lines))
        
    return file_path_valid

async def update_python_files(input_file_path):
    """
    Asynchronously read a text file that contains the code of multiple Python files, and write
    each Python file's code back to its original file.
    
    Parameters:
    - input_file_path (str): The path to the input file containing the Python code
    """
    async with aiofiles.open(input_file_path, 'r') as infile:
        lines = await infile.readlines()

    filepath = ''
    buffer = []
    update_count = 0
    
    # Loop through each line in the input file
    for line in lines:
        if line.startswith("#") and "File: " in line:
            # Extract the filepath from the line
            filepath = line.split('File: ')[1].strip()
        
        elif line.startswith("# End of"):
            # When the end of a file's content is reached
            
            # Skip if filepath is empty or non-existent
            if not filepath:
                print("Skipping an empty or non-existent filepath.")
                continue

            # Skip if buffer is empty (i.e., no content to write)
            if not buffer:
                print(f"No content to write for {filepath}. Skipping...")
                continue

            # Check if the directory exists. If not, create it.
            directory = os.path.dirname(filepath)
            if not os.path.exists(directory):
                print(f"The directory {directory} does not exist. Creating it.")
                os.makedirs(directory)

            # Write the content to the original file
            async with aiofiles.open(filepath, 'w') as outfile:
                await outfile.write(f"# {filepath}\n")  # Insert filepath at the top for documentation
                await outfile.write(''.join(buffer))
                update_count += 1
                print(f"Updated {filepath}")

            # Clear the buffer and filepath for the next file
            buffer.clear()
            filepath = ''
            
        else:
            # Add line to buffer (holding content of the current file being processed)
            buffer.append(line)
    
    print(f"Updated {update_count} Python files.")

if __name__ == '__main__':
    # Restore py files to an alternate folder
    project_folder_name = '/DC_Automation/'
    alternate_project_folder_name = '/DC_Automation2/'
    inputf = 'C:/Users/jacki/Downloads/Homelab/DC_Automation/output/all_bns_scripts_20231016_004244.txt'
    outf = f'{inputf.split(".")[0]}_for_restore_test.txt'
    
    file_path_valid = set_project_root_directory(inputf, outf, project_folder_name, alternate_project_folder_name)
    if file_path_valid:
        asyncio.run(update_python_files(outf))
    else:
        print(f"WARNING: Operation Aborted! Please check and make sure Project folder name is indeed {project_folder_name} in the concatenated python file name in order to avoid any potential data loss before updating the project python files!")
