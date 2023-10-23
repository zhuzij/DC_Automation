# generate_cmd_batches_from_file.py

def read_command_batches_from_file(file_path):
    """
    Read the FortiGate policy configurations from a text file and split them into command batches
    using the keyword 'next' as a delimiter.

    :param file_path: Path to the text file containing the commands
    :return: List of command batches; each batch is a list of commands for the same policy ID
    """
    command_batches = []
    command_batch = []

    # Open the text file and read line by line
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing white spaces
            if line:  # Skip empty lines
                command_batch.append(line)
                if line == 'next':  # Cut at 'next' keyword
                    cmd_batch = '\n'.join(command_batch)
                    # command_batches.append(command_batch.copy())
                    command_batches.append(cmd_batch)
                    command_batch.clear()

    return command_batches

# Example usage
file_path = "C:/Users/jacki/Downloads/labfgt_pol_config.txt"  # Replace this with the path to your file
command_batches = read_command_batches_from_file(file_path)
print(command_batches)
