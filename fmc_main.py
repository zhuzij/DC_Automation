import yaml
from fmc.fmc_tools.fmcobjectmanager import FMCObjectManager
from fmc.fmc_tools.fwobjectsjsonparser import FWObjectsJsonParser
from common.environment_manager import Environment_Manager
from common.task_manager import Task_Manager


def main():
    env_file = "fmc/config/environment.yml"
    task_file = "fmc/config/tasks.yml"

    # Instantiate Environment_Manager
    env_mgr = Environment_Manager(env_file)
    selected_env_name = env_mgr.get_env()
    cred = env_mgr.get_cred()

    # Instantiate Task_Manager
    task_mgr = Task_Manager(task_file)
    selected_task = task_mgr.get_task()

    # Perform the selected task
    if selected_task == 'create firewall object json file':
        fmc_manager = FMCObjectManager(cred, selected_env_name)
        # print(fmc_manager.env)
        fmc_manager.run()
    if selected_task == 'deduplicate_policies':
        fortigateobjectmanager = FortigateObjectManager(selected_env_name, cred)
        fortigateobjectmanager.run()
        fortigatepolicymanager = FortigatePolicyManager(fortigateobjectmanager.firewall_obj_dict, selected_env_name)
        fortigatepolicymanager.run()
    if selected_task == 'deep_diff policies LIST[DICT]':
        folder_path = input("Enter the path to the folder for diff: ")
        json_diff = JSONDeepDiff(folder_path, selected_env_name)
        json_diff.run()
    if selected_task == 'convert object json to fortigate format':
        fwjsonfile = "C:/Users/jacki/Downloads/Homelab/DC_Automation/fmc/output/FMC-Test7.2.0_firewall_obj_dict.json"
        parser = FWObjectsJsonParser(selected_env_name, fwjsonfile)
        # print(fmc_manager.env)
        parser.run()
    
if __name__ == "__main__":
    main()