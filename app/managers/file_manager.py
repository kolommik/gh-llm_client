"""
Handles file-related operations, such as reading files from a directory, filtering by extensions,
and calculating token counts for the contents of each file.
"""

import os
from typing import List, Dict, Any
import tiktoken


# TODO FileManager занимается чтением файлов и их анализом на токены.
# TODO Эти две задачи можно разделить на два разных класса:
# TODO один для работы с файловой системой, другой для обработки текста
# TODO и подсчёта токенов.


def num_tokens_from_content(content: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Computes the number of tokens in the given text for the specified model.

    Parameters
    ----------
    content : str
        Text content.
    model : str, optional
        Model name. Default is "gpt-3.5-turbo".

    Returns
    -------
    int
        Number of tokens in the text.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(content))


class FileManager:
    """
    Class for managing file operations.

    Methods
    -------
    read_files(folder_path: str, target_extensions: str, always_include: str, excluded_dirs: str)
        -> List[Dict[str, Any]]
        Reads files from the specified directory and its subdirectories, filtering by file extensions,
        including specified always-included files, and excluding specified directories.
    """

    def __init__(self):
        pass

    def _prepare_files_list(
        self,
        folder_path: str,
        target_extensions: List[str],
        always_include: List[str],
        excluded_dirs: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Prepares a list of files for processing.

        Parameters
        ----------
        folder_path : str
            Path to the directory.
        target_extensions : List[str]
            List of target file extensions.
        always_include : List[str]
            List of files that should always be included.
        excluded_dirs : List[str]
            List of directories to be excluded.

        Returns
        -------
        List[Dict[str, Any]]
            List of dictionaries representing files.
        """
        files_list = []
        for subdir, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                full_path = os.path.join(subdir, file)
                if file.endswith(tuple(target_extensions)) or file in always_include:
                    with open(full_path, "r", encoding="utf-8") as f:
                        files_list.append(
                            {
                                "path": os.path.relpath(full_path, folder_path),
                                "filename": file,
                                "content": f.read(),
                            }
                        )
        return files_list

    def _augment_files_data(
        self, files_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Processes a list of file dictionaries, reads the content of each file, and augments the dictionary
        with content length, word count, and token count.

        Parameters
        ----------
        files_data : List[Dict[str, Any]]
            List of dictionaries, each containing keys 'path', 'filename', and 'content'.

        Returns
        -------
        List[Dict[str, Any]]
            The same list of dictionaries, but each dictionary is augmented with 'length' (number of characters),
            'words' (number of words), 'lines' (number of lines) and
            'tokens' (number of tokens, computed using the num_tokens_from_content function).
        """

        for file_dict in files_data:
            content = file_dict["content"]
            file_dict["length"] = len(content)
            file_dict["words"] = len(content.split())
            file_dict["tokens"] = num_tokens_from_content(content)
            file_dict["lines"] = (content.count("\n") + 1) if len(content) > 0 else 0

        return files_data

    def read_files(
        self,
        folder_path: str,
        target_extensions: str,
        always_include: str,
        excluded_dirs: str,
    ) -> List[Dict[str, Any]]:
        """
        Reads files from the specified directory and its subdirectories, filtering by file extensions,
        including specified always-included files, and excluding specified directories.

        Parameters
        ----------
        folder_path : str
            Path to the directory.
        target_extensions : str
            String with target file extensions, separated by commas.
        always_include : str
            String with names of files that should always be included, separated by commas.
        excluded_dirs : str
            String with names of directories to be excluded, separated by commas.

        Returns
        -------
        List[Dict[str, Any]]
            List of dictionaries representing files with additional information.
        """
        folder_path = os.path.abspath(folder_path)
        target_extensions = target_extensions.split(", ")
        always_include = always_include.split(", ")
        excluded_dirs = excluded_dirs.split(", ")

        files_list = self._prepare_files_list(
            folder_path, target_extensions, always_include, excluded_dirs
        )
        files_list = self._augment_files_data(files_list)
        return files_list
