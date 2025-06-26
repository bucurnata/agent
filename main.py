import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from schemas import available_functions
from functions.call_function import call_function


def main():
    load_dotenv()

    args = sys.argv[1:]

    if len(sys.argv) < 2:
        print("Error: Prompt is not provided", file=sys.stderr)
        sys.exit(1)

    verbose = "--verbose" in args
    if verbose:
        args.remove("--verbose")

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )

    function_call_part = next(
        (part.function_call for part in response.candidates[0].content.parts if part.function_call),
        None
    )
    #for function_call_part in response.function_calls:
     #  print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    if function_call_part:
        function_call_result =call_function(function_call_part, verbose=True)
        if (
            hasattr(function_call_result.parts[0],"function_response") and function_call_result.parts[0].function_response.response
        ):
            print("->", function_call_result.parts[0].function_response.response)
        else:
            raise RuntimeError("Fatal: Missing function response in call_function return.")
    else:
        print("Response:")    
        print(response.text)

    if verbose and hasattr(response, 'usage_metadata') and response.usage_metadata is not None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

if __name__ == "__main__":
    main()