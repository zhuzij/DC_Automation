import yaml
import json
from typing import Union


def json_file_to_dict(file_path: str) -> Union[dict, None]:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"An error occurred while decoding JSON: {e}")
        return None

def load_yaml_file(filepath):
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)

def prompt_menu(options, prompt_message):
        print()
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        print()
        choice = int(input(f'{prompt_message}'))
        return options[choice - 1]

