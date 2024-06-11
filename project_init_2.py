import os
from omegaconf import OmegaConf
from box import Box


def create_file_if_not_exists(path):
    if not os.path.exists(path):
        open(path, "a").close()
        print(f"File created: {path}")
    else:
        print(f"File already exists: {path}")


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Folder created: {path}")
    else:
        print(f"Folder already exists: {path}")


def create_structure(base_path, conf):
    for k, v in conf.items():
        if v.type == "file":
            create_file_if_not_exists(os.path.join(base_path, k))
        elif v.type == "folder":
            create_folder_if_not_exists(os.path.join(base_path, k))
            child_conf = {k: v for k, v in v.items() if k != "type"}
            create_structure(os.path.join(base_path, k), child_conf)
        else:
            print(f"Invalid type: {v.type}")

if __name__ == "__main__":
    CURRENT_FOLDER = os.getcwd()
    CONF = OmegaConf.load("project_structure.yml")
    create_structure(base_path=CURRENT_FOLDER, conf=CONF)
