import os


def split_file_name(path: str) -> (str, str):
    file_name_with_ext, file_extension_with_dot = os.path.splitext(path)

    if file_extension_with_dot:
        file_extension = file_extension_with_dot[1:]
    else:
        file_extension = ""

    return file_name_with_ext, file_extension
