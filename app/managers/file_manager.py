import os
from typing import List, Dict, Any
import tiktoken


# TODO FileManager занимается чтением файлов и их анализом на токены.
# TODO Эти две задачи можно разделить на два разных класса:
# TODO один для работы с файловой системой, другой для обработки текста
# TODO и подсчёта токенов.


def num_tokens_from_content(content: str, model: str = "gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(content))


class FileManager:
    def __init__(self, folder_path, target_extensions, always_include, excluded_dirs):
        self.folder_path = folder_path
        self.target_extensions = target_extensions.split(", ")
        self.always_include = always_include.split(", ")
        self.excluded_dirs = excluded_dirs.split(", ")

    def _prepare_files_list(self):
        files_list = []
        for subdir, dirs, files in os.walk(self.folder_path):
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            for file in files:
                full_path = os.path.join(subdir, file)
                if (
                    file.endswith(tuple(self.target_extensions))
                    or file in self.always_include
                ):
                    with open(full_path, "r", encoding="utf-8") as f:
                        files_list.append(
                            {
                                "path": os.path.relpath(full_path, self.folder_path),
                                "filename": file,
                                "content": f.read(),
                            }
                        )
        return files_list

    def _augment_files_data(
        self, files_data: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Process a list of file dictionaries, reading content from each and augmenting the dictionary
        with the length of content, the number of words, and the number of tokens.

        Parameters
        ----------
        files_data : list of dict
            A list of dictionaries, each containing 'path', 'filename', and 'content' keys.

        Returns
        -------
        list of dict
            The same list of dictionaries, but each dictionary is augmented with 'length' (number of characters),
            'words' (number of words), and 'tokens' (number of tokens using num_tokens_from_content) fields.

        Notes
        -----
        This function assumes that the content of each file is text and uses the 'num_tokens_from_content' function
        to calculate the number of tokens according to a specific model's encoding.

        """
        for file_dict in files_data:
            content = file_dict["content"]
            file_dict["length"] = len(content)
            file_dict["words"] = len(content.split())
            file_dict["tokens"] = num_tokens_from_content(content)
            file_dict["lines"] = (content.count("\n") + 1) if len(content) > 0 else 0

        return files_data

    def read_files(self) -> List[Dict[str, str]]:
        """
        Read files from a given directory and its subdirectories,
        filtering by file extensions, including specified always include files,
        and excluding specified directories.
        """
        files_list = self._prepare_files_list()
        files_list = self._augment_files_data(files_list)
        return files_list
