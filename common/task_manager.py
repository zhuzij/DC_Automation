from common.utils import load_yaml_file, prompt_menu

class Task_Manager:
    def __init__(self, task_file):
        self.task_file = task_file
        self.task_data = load_yaml_file(self.task_file)['tasks']

    def get_task(self):
        task_names = self.task_data
        self.selected_task_name = prompt_menu(task_names, "Choose a task number from the above list: ")
        print(f"Selected task: {self.selected_task_name}")
        return self.selected_task_name