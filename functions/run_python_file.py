import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        result = subprocess.run(["python", full_path],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                cwd=working_directory,
                                timeout=30,
                                text=True
        )

        output = []
        if result.stdout.strip():
            output.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            output.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced."
    
    except Exception as e:
        return f'Error: {str(e)}'

