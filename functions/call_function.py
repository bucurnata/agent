import os
from google.genai import types
from functions import get_files_info
from functions import get_file_content
from functions import run_python_file
from functions import write_file
from config import WORKING_DIR

def call_function(function_call_part: types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling funcyion: {function_name}")

    working_directory = WORKING_DIR
    function_args["working_directory"] = working_directory

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    try:
        function_result = function_map[function_name](**function_args)
    except Exception as e:
        function_result = f"Error: Exception while running {function_name}: {str(e)}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )