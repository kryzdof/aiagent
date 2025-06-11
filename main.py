import os
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions import all_schemas

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) <= 1:
    print("Please provide a prompt")
    sys.exit(1)

if len(sys.argv) > 3:
    print("Please provide the prompt in ''")
    sys.exit(1)

user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

def vprint(text):
    if verbose:
        print(text)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


available_functions = types.Tool(
    function_declarations=[
        all_schemas,
    ]
)

vprint(f"User prompt: {user_prompt}")
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
resp = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages,
                                      config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
print(f"Response {resp.text}")
for function_call_part in resp.function_calls:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
vprint(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
vprint(f"Response tokens: {resp.usage_metadata.candidates_token_count}")