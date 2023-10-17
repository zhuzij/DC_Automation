import yaml
from fortigate.fortigate_tools.fortigate_policy_manager_interface import FortigatePolicyManager
from fortigate.fortigate_tools.fortigateobjectmanager import FortigateObjectManager
from fortigate.fortigate_tools.jsondeepdiff_policies import JSONDeepDiff
from fortigate.fortigate_tools.run_commands_FGT_v1_OOP import FortiGateCLIAsync
from common.environment_manager import Environment_Manager
from common.task_manager import Task_Manager
import asyncio

def main():
    env_file = "config/environment.yml"
    task_file = "config/tasks.yml"

    # Instantiate Environment_Manager
    env_mgr = Environment_Manager(env_file)
    selected_env_name = env_mgr.get_env()
    cred = env_mgr.get_cred()

    # Instantiate Task_Manager
    task_mgr = Task_Manager(task_file)
    selected_task = task_mgr.get_task()

    # Perform the selected task
    if selected_task == 'create firewall object json file':
        fortigateobjectmanager = FortigateObjectManager(selected_env_name, cred)
        fortigateobjectmanager.run()
    elif selected_task == 'deduplicate_policies':
        fortigateobjectmanager = FortigateObjectManager(selected_env_name, cred)
        fortigateobjectmanager.run()
        fortigatepolicymanager = FortigatePolicyManager(fortigateobjectmanager.firewall_obj_dict, selected_env_name)
        fortigatepolicymanager.run()
    elif selected_task == 'deep_diff policies LIST[DICT]':
        folder_path = input("Enter the path to the folder for diff: ")
        json_diff = JSONDeepDiff(folder_path, selected_env_name)
        json_diff.run()
    elif selected_task == 'run_FGT_CLI':
        fgt_cli = FortiGateCLIAsync(host="192.168.3.1", username="joe", password="Iching12#")

        async def run_commands():
            await fgt_cli.connect()
            output = await fgt_cli.run_command("c v\nedit root\nget system status\nget sys interface\nget router info routing-table all\nconfig firewall service custom\nrename plex_port_32400 to plex_port\nrename tcp-8080 to tcp_8080\n")
            print(output)
            await fgt_cli.disconnect()

        asyncio.run(run_commands())
        

if __name__ == "__main__":
    main()
