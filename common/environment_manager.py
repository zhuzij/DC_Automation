from common.utils import load_yaml_file, prompt_menu

class Environment_Manager:
    def __init__(self, env_file):
        self.env_file = env_file
        self.environment_data = load_yaml_file(self.env_file)['environments']

    def get_env(self):
        environment_names = list(self.environment_data.keys())
        print()
        self.selected_env_name = prompt_menu(environment_names, "Choose an environment number from the above list: ")
        print()
        print(f"Selected environment: {self.selected_env_name}")
        return self.selected_env_name

    def get_cred(self):
        self.credential = self.environment_data[self.selected_env_name]
        return self.credential

