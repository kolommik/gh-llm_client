import json
import os
from typing import List, Dict

# Функция для загрузки настроек из JSON-файла
def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        return {
            "folder_path": "",
            "target_extensions": "",
            "always_include": "",
            "excluded_dirs": "",
            "system_prompt": "",
        }


# Функция для сохранения настроек в JSON-файл
def save_settings(
    folder_path, target_extensions, always_include, excluded_dirs, system_prompt
):
    settings = {
        "folder_path": folder_path,
        "target_extensions": target_extensions,
        "always_include": always_include,
        "excluded_dirs": excluded_dirs,
        "system_prompt": system_prompt,
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)


def read_files(folder_path: str, target_extensions: List[str], always_include_files: List[str], excluded_directories: List[str]) -> List[Dict[str, str]]:
    """
    Recursively read files from a given directory and its subdirectories, 
    filtering by file extensions, including specified always include files, 
    and excluding specified directories.

    Parameters
    ----------
    folder_path : str
        The root directory from which to start reading files.
    target_extensions : list of str
        List of file extensions to include in the search (e.g., ['.py', '.txt']).
    always_include_files : list of str
        List of file names to always include in the final output regardless of their extensions or directories.
    excluded_directories : list of str
        List of directory names to exclude from the search.

    Returns
    -------
    list of dict
        A list of dictionaries, each dictionary contains 'path' (the relative path of the file), 
        'filename' (the name of the file), and 'content' (the content of the file).

    Notes
    -----
    The function reads the content of each file that matches the target extensions or is listed in the 
    always include files, excluding files in any of the excluded directories. It's designed to be used 
    for text files as it reads contents into a string.

    """
    files_list = []
    for subdir, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded_directories]
        for file in files:
            full_path = os.path.join(subdir, file)
            if file.endswith(tuple(target_extensions)) or file in always_include_files:
                with open(full_path, 'r', encoding="utf-8") as f:
                    files_list.append({
                        'path': os.path.relpath(full_path, folder_path),
                        'filename': file,
                        'content': f.read()
                    })
    return files_list
