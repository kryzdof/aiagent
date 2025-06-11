import os
import subprocess
import time

def run_python_file(working_directory, file_path):
    workingDir = os.path.abspath(working_directory) 
    targetFile = os.path.abspath(os.path.join(workingDir, file_path))
    if workingDir not in targetFile:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(targetFile):
        return f'Error: File "{file_path}" not found.'
    if not targetFile.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        time.sleep(30)
        result = subprocess.run(["python", file_path], capture_output=True, cwd=workingDir)
        retString = ""
        if result.stdout or result.stderr: 
            if result.stdout:
                retString += f"STDOUT: {result.stdout}"
            if result.stderr:
                retString += f"STDERR: {result.stderr}"
        else:
            retString += "No output produced"
        if result.returncode != 0:
            retString += f"Process exited with code {result.returncode}"
        return retString
    except Exception as e:
        return f"Error: executing Python file: {e}"
    


from google.genai import types
schema = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file, relative to the working directory.",
            ),
        },
    ),
)