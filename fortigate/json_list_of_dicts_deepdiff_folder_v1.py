#***********************************************************
#     Filename: json_list_of_dicts_deepdiff_folder_v1.py
#     Purpose: Present diff based upon a folder name
#     Date of creation: 9-10-2023
#     Author-Joe Zhu
#***********************************************************
 
import os
from deepdiff import DeepDiff
import json
 
'''
The script will present diff operation between two json files for the same firewall configuration section, e.g. address, policy and etc.
 
Input:
The base folder:
C:\Users\s4739693\Downloads\fgt_diff\foldername
You'd need to create this folder based upon timestamp, such as 2023_09_30_07_57
 
Save your files for diff into subfolders:
For file1: b4
For file1: afer
 
Output:
Diff file will be saved to the script's basedir\output):
e.g. C:\Users\s4739693\MyPythonProj\explore\IGW\output
Name of the diff file: e.g. PPE_policy_standard_list_2023_09_23_2023_09_30_deepdiff.txt
'''
 
def replace_backslash(filepath):
    """
    Replaces backslashes with forward slashes in a filepath.
 
    Args:
        filepath (str): The filepath to be processed.
 
    Returns:
        str: The filepath with backslashes replaced by forward slashes.
    """
    return filepath.replace("\\", "/")
 
def compare_dicts(dict1, dict2, prefix=""):
    """
    Recursively compares two dictionaries and generates a list of differences.
 
    Args:
        dict1 (dict): The first dictionary to compare.
        dict2 (dict): The second dictionary to compare.
        prefix (str): A prefix to add to the difference keys.
 
    Returns:
        list: A list of differences between the dictionaries.
    """
    diff_list = []
 
    for key in dict1.keys():
        if key not in dict2:
            diff_list.append(f"- {prefix}{key}: {dict1[key]}")
 
    for key in dict2.keys():
        if key not in dict1:
            diff_list.append(f"+ {prefix}{key}: {dict2[key]}")
 
    for key in dict1.keys() & dict2.keys():
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            diff_list.extend(compare_dicts(dict1[key], dict2[key], prefix=f"{prefix}{key}."))
        elif dict1[key] != dict2[key]:
            diff_list.append(f"- {prefix}{key}: {dict1[key]}")
            diff_list.append(f"+ {prefix}{key}: {dict2[key]}")
 
    return diff_list
 
# prompt for the folder for diff:
print(os.getcwd())
folder_path = replace_backslash(input("Enter the path to the folder for diff: "))
short_folder1 = "b4"
short_folder2 = "after"
folder1_path = folder_path + f"/{short_folder1}"
folder2_path = folder_path + f"/{short_folder2}"
 
script_file_path = os.path.abspath(__file__)
script_folder_path = os.path.dirname(script_file_path)
 
# Check if the provided paths are valid folders
if not os.path.isdir(folder1_path) or not os.path.isdir(folder2_path):
    print("Invalid folder paths. Please provide valid paths to folders.")
else:
    # Get a list of file names in each folder
    folder1_files = os.listdir(folder1_path)
    folder2_files = os.listdir(folder2_path)
 
    # Iterate through the files in both folders
    for file_name in folder1_files:
        file1_path = os.path.join(folder1_path, file_name)
       
    for file_name in folder2_files:
        file2_path = os.path.join(folder2_path, file_name)
 
    # resolve filename datetime part
    file1_name = os.path.basename(file1_path).split('.')[0]
    filename2_datetime = os.path.basename(file2_path).split('list_')[1].split('.')[0]
 
    # Load the JSON data from both files
    with open(file1_path, 'r') as file1:
        json_data1 = json.load(file1)
    with open(file2_path, 'r') as file2:
        json_data2 = json.load(file2)
 
    # Extract the 'ID' from each JSON object within the list
    ids1 = [item.get('ID') for item in json_data1]
    ids2 = [item.get('ID') for item in json_data2]
 
    # Find all unique IDs from both sets
    all_ids = set(ids1) | set(ids2)
    ids_only_in_before = set(ids1) - set(ids2)
    ids_only_in_after = set(ids2) - set(ids1)
 
    # Initialize a flag to check if any differences were found
    differences_found = False
 
    # Generate the output file name for this file
 
    output_file_name = os.path.join(script_folder_path, f"output/PPE_{file1_name}_{filename2_datetime}_deepdiff.txt")
 
    with open(output_file_name, 'w') as output_file:
        # Write IDs only in the "before" file
        if ids_only_in_before:
            differences_found = True
            output_file.write("IDs in before and not in after:\n")
            for common_id in ids_only_in_before:
                output_file.write(f"- ID: {common_id}\n")
 
        # Write IDs only in the "after" file
        if ids_only_in_after:
            differences_found = True
            output_file.write("IDs in after and not in before:\n")
            for common_id in ids_only_in_after:
                output_file.write(f"+ ID: {common_id}\n")
 
        # Iterate through all unique IDs and compare the rest of the differences
        for common_id in all_ids:
            # Filter JSON data based on the 'ID' for comparison
            data1 = [item for item in json_data1 if item.get('ID') == common_id]
            data2 = [item for item in json_data2 if item.get('ID') == common_id]
 
            # Compare the filtered JSON data using deepdiff
            if data1 and data2:
                diff = compare_dicts(data1[0], data2[0])
 
                # Check if there are differences
                if diff:
                    differences_found = True
 
                    # Write section header only if there are differences
                    if common_id not in ids_only_in_before and common_id not in ids_only_in_after:
                        output_file.write(f"\nDifferences in {file_name} (ID: {common_id}):\n")
 
                    # Write the differences to the output file
                    output_file.write("\n".join(diff))
                    output_file.write("\n")  # Add a blank line between records
 
        # If no differences were found, delete the output file
        if not differences_found:
            try:
                os.remove(output_file_name)
                print(f"No Difference Found for {file1_name}!!!")
            except Exception as e:
                print(e)
        else:
            print(f"Differences for {file1_name} have been saved to {output_file_name}.")
 