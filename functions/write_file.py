import os

def write_file(working_directory, file_path, content):
    workingDir = os.path.abspath(working_directory) 
    targetFile = os.path.abspath(os.path.join(workingDir, file_path))
    if workingDir not in targetFile:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    os.makedirs(os.path.dirname(targetFile), exist_ok=True)
    
    try: 
        with open(targetFile, "w") as fp:
            fp.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


from google.genai import types
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to the file specified in the file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written into the file.",
            ),
        },
    ),
)