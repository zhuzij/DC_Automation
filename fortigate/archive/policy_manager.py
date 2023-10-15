from common.utils import Environment_Task_Manager, deep_diff, deduplicate

class PolicyManager:
    def __init__(self, credentials):
        self.username = credentials['username']
        self.password = credentials['password']
        self.host = credentials['host']
        self.policies = []

    def deduplicate_policies(self):
        deduplicate(self.policies)

    def deep_diff(self):
        deep_diff({"key": "value"}, {"key": "new_value"})


# Usage
env_manager = Environment_Task_Manager('config/environment.yml', 'config/tasks.yml')
selected_env = env_manager.get_env()
selected_task = env_manager.get_task()
