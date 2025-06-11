import os

def get_files_info(working_directory, directory=None):
    workingDir = os.path.abspath(working_directory) 
    targetDir = os.path.abspath(os.path.join(workingDir, directory))
    if workingDir not in targetDir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(targetDir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        rsl = []  # returnStringList
        for file in os.listdir(targetDir):
            fp = os.path.join(targetDir, file)
            rsl.append(f"- {file}: file_size={os.path.getsize(fp)} bytes, is_dir={os.path.isdir(fp)}")
        return "\n".join(rsl)
    except Exception as e:
        return f"Error: {e}"
    


from google.genai import types
schema = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)