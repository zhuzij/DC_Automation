import yaml

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
