import os
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

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


vprint(f"User prompt: {user_prompt}")
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
resp = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
print(resp.text)
vprint(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
vprint(f"Response tokens: {resp.usage_metadata.candidates_token_count}")