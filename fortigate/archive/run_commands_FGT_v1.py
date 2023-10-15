#*****************************************************
#     Filename: run_commands_FGT_v1.py
#     Purpose: Run arbitary FGT CLI and display results
#     Date of creation: 8-20-2023
#     Author-Joe Zhu
#*****************************************************
 
import paramiko
import time
import yaml
import select
import datetime
import os
import sys
sys.path.append('C:/Users/s4739693/MyPythonProj')
from utils.menu_tools import get_env_options
 
""""
If output gets cut off, go to send_command(), make sure use receive_all_data() for output; then in receive_all_data() adjust the buffer size as needed.
"""
def save_output_to_file(output):
    timestamp = datetime.datetime.now().strftime("%Y_%b_%d_%H_%M_%S")
    filename = f"output\\output_{timestamp}.txt"
 
    with open(filename, "w") as file:
        file.write(output)
 
def run_commands(fortigate_ip, username, password, commands_string, send_per_command=False):
    """
    Connect to the FortiGate device and run commands.
 
    Args:
        fortigate_ip (str): IP address of the FortiGate device.
        username (str): Username for SSH login.
        password (str): Password for SSH login.
        commands_string (str): String containing the commands to be executed.
        send_per_command (bool, optional): If True, sends commands one by one.
                                          If False, sends all commands in a single batch.
 
    Returns:
        None
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(fortigate_ip, username=username, password=password)
        chan = ssh.invoke_shell()
 
        if send_per_command:
            cmds = get_commands_string(commands_string)
            for cmd in cmds:
                send_command(chan, cmd)
        else:
            send_command(chan, commands_string)
 
        ssh.close()
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_ex:
        print(f"SSH connection error: {ssh_ex}")
    except Exception as ex:
        print(f"Error: {ex}")
 
def receive_all_data(chan):
    """
    Receive all data from the SSH channel.
 
    This function continuously reads data from the SSH channel until there is no more data available.
    It ensures that all data is received, even if the output size is larger than the specified buffer size.
 
    Args:
        chan (paramiko.Channel): Paramiko channel object for SSH communication.
 
    Returns:
        str: The received data as a decoded string.
 
    Raises:
        paramiko.SSHException: If there is an issue with the SSH channel.
        UnicodeDecodeError: If there is an error decoding the received data.
 
    Example:
        # Assuming 'chan' is the SSH channel
        output = receive_all_data(chan)
    """
    # buffer adjustable per the need
    buffer_size = 99999
    data = b""
    while True:
        try:
            # Use select to check if there is data available to be received
            readable, _, _ = select.select([chan], [], [], 0.1)
            if not readable:
                # No data available, break the loop
                break
 
            chunk = chan.recv(buffer_size)
        except paramiko.SSHException as ssh_ex:
            raise ssh_ex
        except Exception as ex:
            raise ex
 
        if not chunk:
            break
        data += chunk
    return data.decode()
 
def send_command(chan, command):
    """
    Send a command over the SSH channel and print the output.
 
    Args:
        chan (paramiko.Channel): Paramiko channel object for SSH communication.
        command (str): Command to be sent.
 
    Returns:
        None
    """
    chan.send(f"{command}\n")
    time.sleep(1)
    # output = chan.recv(99999).decode() # use this line of code a fallback if the next line not work!!!
    output = receive_all_data(chan)
 
    print(output)
    save_output_to_file(output)
 
def get_commands_string(commands_string):
    """
    Split the commands string into individual commands.
 
    Args:
        commands_string (str): String containing multiple commands.
 
    Returns:
        list: List of individual commands.
    """
    cmds = commands_string.splitlines()
    cmds = [cmd.strip() for cmd in cmds]
    return cmds
 
# Function to load configuration from YAML file
def load_config(config_file, env):
    """
    Load configuration parameters from a YAML file based on the specified env.
 
    Args:
        config_file (str): Path to the YAML configuration file.
        env (str): env name to load the configuration for.
 
    Returns:
        dict: A dictionary containing the configuration parameters for the given env.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config.get(env, {})
 
def main():
    # print(os.getcwd())
    config_file = "explore/IGW/config.yaml"
 
    while True:
        print("Please choose your environment:")
       
        # Get the env options dynamically from the config.yaml
        env_options = get_env_options(config_file)
 
        for i, env in enumerate(env_options, 1):
            print(f"{i}. {env.upper()}")
 
        user_input = input('Please enter your choice (e.g. 1 or 2 or 1,2 or q to quit): ')
        user_input = user_input.replace(" ", "").split(",")
 
        should_exit = False  # Flag to indicate if the user wants to quit the program
 
        for input_item in user_input:
            if input_item.isdigit():
                index = int(input_item)
                if 1 <= index <= len(env_options):
                    # Get the chosen env
                    env = env_options[index - 1]
                    config_data = load_config(config_file, env)
                    run_commands(**config_data)
                else:
                    print("Invalid env choice. Please try again!\n")
                    break  # Exit the for loop and re-prompt the user
            elif input_item.lower() == 'q':
                should_exit = True
                break  # Exit the for loop and terminate the program gracefully
            else:
                print("Invalid input. Please try again!\n")
                break  # Exit the for loop and re-prompt the user
 
        if should_exit:
            break  # Exit the while loop and terminate the program
 
if __name__ == '__main__':
    main()