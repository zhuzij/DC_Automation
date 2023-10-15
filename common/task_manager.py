from common.utils import load_yaml_file, prompt_menu
from typing import List

class Task_Manager:
    def __init__(self, task_file: str):
        self.task_file = task_file
        self.task_data: List = load_yaml_file(self.task_file)['tasks']

    def get_task(self):
        self.selected_task_name = prompt_menu(self.task_data, "Choose a task number from the above list: ")
        print(f"Selected task: {self.selected_task_name}")
        return self.selected_task_name