import asyncio
import aiofiles
import os
from datetime import datetime

def generate_tree(directory):
    tree_str = ''
    for root, dirs, files in os.walk(directory):
        # Skip the specified folder
        if 'fortigate-api' in dirs:
            dirs.remove('fortigate-api')

        python_files = [f for f in files if f.endswith('.py')]
        if python_files:
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree_str += f'{indent}{root}/\n'  # Updated to include full path
            subindent = ' ' * 4 * (level + 1)
            for f in python_files:
                tree_str += f'{subindent}{f}\n'
    return tree_str

async def concatenate_python_files():
    # Get the current working directory
    start_dir = os.getcwd()
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(start_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    # Get the current timestamp and format it
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Construct the output file path
    output_file_path = os.path.join(output_dir, f'all_bns_scripts_{timestamp}.txt')

    # Open the output file
    async with aiofiles.open(output_file_path, mode='w') as outfile:
        # Initialize a counter for the total number of Python files
        file_count = 0
        # Initialize a sequence number
        sequence_number = 0
        # Walk through the start directory and all subdirectories
        for root, dirs, files in os.walk(start_dir):
            # Skip the specified folder
            if 'fortigate-api' in dirs:
                dirs.remove('fortigate-api')

            # Filter out Python files and exclude the output file
            python_files = [f for f in files if f.endswith('.py') and not f.startswith('all_bns_')]
            # Update the file count
            file_count += len(python_files)
            # Iterate through each file
            for filename in python_files:
                # Increment the sequence number
                sequence_number += 1
                filepath = os.path.join(root, filename)
                # Open, read, and write each file's contents to the output file
                async with aiofiles.open(filepath, mode='r') as infile:
                    contents = await infile.read()
                    await outfile.write(f"# {sequence_number}. File: {filepath}\n")
                    await outfile.write(contents)
                    await outfile.write(f"\n# End of {filepath}\n\n")
        # Write the total file count to the output file
        await outfile.write(f"# Total number of Python files concatenated: {file_count}\n")

        # Generate the directory structure and write it to the output file
        tree_str = generate_tree(start_dir)
        await outfile.write(f"\n# Directory Structure:\n{tree_str}")

# Run the function
if __name__ == '__main__':
    asyncio.run(concatenate_python_files())
