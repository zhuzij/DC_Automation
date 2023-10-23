import asyncio
from concurrent.futures import ThreadPoolExecutor
import paramiko
import logging
logging.basicConfig(level=logging.DEBUG)

import os
import sys
sys.path.append(os.getcwd())
from common.timeit import timeit
from fortigate.fortigate_tools.generate_commands import commands_string


class FortiGateCLIAsync:
    def __init__(self, host, username, password, timeout=10):
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
        stdin, stdout, stderr = ssh_client.exec_command(command)
        return stdout.read().decode('utf-8')

    async def run_command(self, command):
        if self.loop is None:
            self.loop = asyncio.get_running_loop()
        if not self.is_connected:
            print("Not connected. Please connect first.")
            return
        try:
            output = await self.loop.run_in_executor(self.executor, self._exec_command, self.ssh_client, command)
            return output
        except Exception as e:
            print(f"Failed to run command due to exception: {e}")


    async def disconnect(self):
        if self.loop is None:
            self.loop = asyncio.get_running_loop()
        await self.loop.run_in_executor(self.executor, self.ssh_client.close)

# Example usage
@timeit
async def main():
    fgt_cli = FortiGateCLIAsync(host="192.168.3.1", username="joe", password="x")
    await fgt_cli.connect()
    output = await fgt_cli.run_command(f"{commands_string}")
    print(output)
    await fgt_cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())