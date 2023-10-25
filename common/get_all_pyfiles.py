import asyncio
import aiofiles
import os
from datetime import datetime

def generate_tree(directory):
    tree_str = ''
    for root, dirs, files in os.walk(directory):
        if 'fortigate-api' in dirs:
            dirs.remove('fortigate-api')
        python_files = [f for f in files if f.endswith('.py')]
        if python_files:
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree_str += f'{indent}{root}/\n'
            subindent = ' ' * 4 * (level + 1)
            for f in python_files:
                tree_str += f'{subindent}{f}\n'
    return tree_str

async def concatenate_python_files():
    start_dir = os.getcwd()
    output_dir = os.path.join(start_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file_path = os.path.join(output_dir, f'all_bns_scripts_{timestamp}.txt')

    async with aiofiles.open(output_file_path, mode='w', encoding='utf-8') as outfile:
        file_count = 0
        sequence_number = 0
        for root, dirs, files in os.walk(start_dir):
            for dir_to_skip in ['fortigate-api', 'venv']: # !!! add folders to be skipped here !!!!
                if dir_to_skip in dirs:
                    dirs.remove(dir_to_skip)
            python_files = [f for f in files if f.endswith('.py') and not f.startswith('all_bns_')]
            file_count += len(python_files)
            for filename in python_files:
                sequence_number += 1
                filepath = os.path.join(root, filename)
                async with aiofiles.open(filepath, mode='r', encoding='utf-8') as infile:  # Added encoding here
                    contents = await infile.read()
                    await outfile.write(f"# {sequence_number}. File: {filepath.replace('\\', '/')}\n")
                    await outfile.write(contents)
                    await outfile.write(f"\n# End of {filepath}\n\n")
        await outfile.write(f"# Total number of Python files concatenated: {file_count}\n")
        tree_str = generate_tree(start_dir)
        await outfile.write(f"\n# Directory Structure:\n{tree_str}")

if __name__ == '__main__':
    asyncio.run(concatenate_python_files())
