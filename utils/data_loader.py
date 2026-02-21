import yaml
import os


def load_test_data(file_name):

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(project_root, file_name)

    with open(file_path, "r") as file:
        return yaml.safe_load(file)
