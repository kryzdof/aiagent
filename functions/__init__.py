from google.genai import types

from .get_files_info import schema_get_files_info, get_files_info
from .get_file_content import schema_get_file_content, get_file_content
from .write_file import schema_write_file, write_file
from .run_python import schema_run_python_file, run_python_file

all_schemas = [schema_get_files_info,
               schema_get_file_content,
               schema_write_file,
               schema_run_python_file]

all_functions = {"get_files_info": get_files_info,
                 "get_file_content": get_file_content,
                 "write_file": write_file,
                 "run_python_file": run_python_file}


def call_function(function_call_part, verbose):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    if function_call_part.name in all_functions:
        function_call_part.args.update({"working_directory": "./calculator"})
        function_result = all_functions[function_call_part.name](**function_call_part.args)
        return types.Content(
        role="tool", parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
                )
            ],
        )
    return types.Content(
        role="tool", parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )