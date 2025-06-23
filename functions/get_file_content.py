import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS + 1)
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'

        return content

    except Exception as e:
        return f'Error reading file "{file_path}": {str(e)}'
