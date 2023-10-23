import asyncio
from concurrent.futures import ThreadPoolExecutor
import paramiko
import logging
logging.basicConfig(level=logging.DEBUG)

import os
import sys
sys.path.append(os.getcwd())

# Assuming these imports match with your own modules and logic
from common.timeit import timeit
from common.generate_cmd_batches_from_file import command_batches  # Assuming commands_string is a list of command batches


class FortiGateCLIAsync:
    """
    Asynchronous SSH client for interacting with FortiGate devices.
    """
    def __init__(self, host, username, password, timeout=10):
        """
        Initialize connection settings and SSH client.

        :param host: IP address of the FortiGate device
        :param username: SSH username
        :param password: SSH password
        :param timeout: Timeout for the SSH connection, in seconds
        """
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.loop = None  # Initialized to None
        self.executor = ThreadPoolExecutor()
        self.is_connected = False  # Initialize to False

    async def connect(self):
        """
        Asynchronously establish an SSH connection using ThreadPoolExecutor.
        """
        self.loop = asyncio.get_running_loop()
        try:
            def wrapper():
                self.ssh_client.connect(hostname=self.host, username=self.username, password=self.password, timeout=self.timeout)
                
            await self.loop.run_in_executor(self.executor, wrapper)

            if self.ssh_client.get_transport() is not None:
                print("Successfully connected.")
                self.is_connected = True
            else:
                print("Failed to connect.")
                self.is_connected = False
        except Exception as e:
            self.is_connected = False
            print(f"Failed to connect due to exception: {e}")

    def _exec_command(self, ssh_client, command):
        """
        Execute a single command over SSH and return the output.

        :param ssh_client: Active Paramiko SSH client
        :param command: Command to run
        :return: Command output as a string
        """
        stdin, stdout, stderr = ssh_client.exec_command(command)
        return stdout.read().decode('utf-8')

    async def run_command_batch(self, command_batch):
        """
        Asynchronously execute a batch of commands over SSH.

        :param command_batch: List of commands to run sequentially
        :return: Concatenated output from all commands
        """
        if self.loop is None:
            self.loop = asyncio.get_running_loop()
        if not self.is_connected:
            print("Not connected. Please connect first.")
            return
        try:
            output = ''
            for cmd in command_batch:
                output += await self.loop.run_in_executor(self.executor, self._exec_command, self.ssh_client, cmd)
            return output
        except Exception as e:
            print(f"Failed to run command batch due to exception: {e}")

    async def disconnect(self):
        """
        Asynchronously close the SSH connection.
        """
        if self.loop is None:
            self.loop = asyncio.get_running_loop()
        await self.loop.run_in_executor(self.executor, self.ssh_client.close)


# Example usage
@timeit
async def main():
    """
    Example asynchronous routine to connect, send command batches, and disconnect.
    """
    fgt_cli = FortiGateCLIAsync(host="192.168.3.1", username="joe", password="x")
    await fgt_cli.connect()
    
    # Assuming commands_string is a list of command batches; each batch is a list of commands for the same policy ID
    for command_batch in command_batches:
        output = await fgt_cli.run_command_batch(command_batch)
        print(output)
    
    await fgt_cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
