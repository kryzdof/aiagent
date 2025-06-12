import os

MAX_SIZE = 10000

def get_file_content(working_directory, file_path):
    workingDir = os.path.abspath(working_directory) 
    targetFile = os.path.abspath(os.path.join(workingDir, file_path))
    if workingDir not in targetFile:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(targetFile):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try: 
        with open(targetFile) as fp:
            text = fp.read(MAX_SIZE + 1)
        if len(text) > MAX_SIZE:
            text = text[:-1] + f'[...File "{file_path}" truncated at 10000 characters]'
        return text
    except Exception as e:
        return f"Error: {e}"
    

from google.genai import types
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the specified file up to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read from, relative to the working directory.",
            ),
        },
    ),
)