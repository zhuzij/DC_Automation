import os
import json

class JSONDeepDiff:
    '''
    Class to deepdiff policies dictionary (of list of dictionaries) based upon "policyid"
    '''
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.folder1_path = os.path.join(folder_path, "b4")
        self.folder2_path = os.path.join(folder_path, "after")
        self.script_folder_path = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
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

    def process_folders(self):
        if not os.path.isdir(self.folder1_path) or not os.path.isdir(self.folder2_path):
            print("Invalid folder paths. Please provide valid paths to folders.")
            return

        folder1_files = os.listdir(self.folder1_path)
        folder2_files = os.listdir(self.folder2_path)

        for file_name in folder1_files:
            file1_path = os.path.join(self.folder1_path, file_name)

        for file_name in folder2_files:
            file2_path = os.path.join(self.folder2_path, file_name)

        # resolve filename datetime part
        file1_name = os.path.basename(file1_path).split('.')[0]
        filename2_datetime = os.path.basename(file2_path).split('.')[0]
    
        # Load the JSON data from both files
        with open(file1_path, 'r') as file1:
            json_data1 = json.load(file1)
            print(f'{json_data1=}')
        with open(file2_path, 'r') as file2:
            json_data2 = json.load(file2)

        # Extract the 'policyid' from each JSON object within the policies list
        ids1 = [item.get('policyid') for item in json_data1['policies']]
        ids2 = [item.get('policyid') for item in json_data2['policies']]
    
        # Find all unique IDs from both sets
        all_ids = set(ids1) | set(ids2)
        ids_only_in_before = set(ids1) - set(ids2)
        ids_only_in_after = set(ids2) - set(ids1)
    
        # Initialize a flag to check if any differences were found
        differences_found = False
    
        # Generate the output file name for this file
    
        output_file_name = f"{self.folder_path}/{file1_name}_{filename2_datetime}_deepdiff.txt"
    
        with open(output_file_name, 'w') as output_file:
            # Write IDs only in the "before" file
            if ids_only_in_before:
                differences_found = True
                output_file.write("policyids in before and not in after:\n")
                for common_id in ids_only_in_before:
                    output_file.write(f"- ID: {common_id}\n")
    
            # Write IDs only in the "after" file
            if ids_only_in_after:
                differences_found = True
                output_file.write("policyids in after and not in before:\n")
                for common_id in ids_only_in_after:
                    output_file.write(f"+ ID: {common_id}\n")
    
            # Iterate through all unique IDs and compare the rest of the differences
            for common_id in all_ids:
                # Filter JSON data based on the 'ID' for comparison
                data1 = [item for item in json_data1['policies'] if item.get('policyid') == common_id]
                data2 = [item for item in json_data2['policies'] if item.get('policyid') == common_id]
    
                # Compare the filtered JSON data using deepdiff
                if data1 and data2:
                    diff = self.compare_dicts(data1[0], data2[0])
    
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

    def run(self):
        self.process_folders()

if __name__ == "__main__":
    print(os.getcwd())
    folder_path = input("Enter the path to the folder for diff: ")
    json_diff = JSONDeepDiff(folder_path)
    json_diff.run()
