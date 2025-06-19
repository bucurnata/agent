import os

def get_files_info(working_directory, directory=None):
    try:
        working_directory = os.path.abspath(working_directory)

        if directory is None:
            directory_path = working_directory
        else:
            directory_path = os.path.abspath(os.path.join(working_directory, directory))

        if  not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'

        if not directory_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        items = []
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            is_dir = os.path.isdir(item_path)
            try:
                size = os.path.getsize(item_path)
                items.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                return f'Error: Could not access size of "{item_path}": {str(e)}'
            
        return '\n'.join(items)
    
    except Exception as e:
        return f"Error: {str(e)}"
        