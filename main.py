import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from schemas import available_functions
from functions.call_function import call_function
from config import MAX_ITERATIONS


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

    for step in range(MAX_ITERATIONS):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt)
        )

        candidates = response.candidates
        if not candidates:
            print("No response from model")
            break
        for candidate in candidates:
            if candidate.content:
                messages.append(candidate.content)

        function_call_part = None
        for part in candidates[0].content.parts:
            if hasattr(part, "function_call"):
                function_call_part = part.function_call
                break
        
        if function_call_part:
            function_call_result =call_function(function_call_part, verbose=True)
            messages.append(function_call_result)

            if verbose:
                result_data = function_call_result.parts[0].function_response.response
                print(f"-> {result_data}")

        else:
            final_text = candidates[0].content.parts[0].text
            print("Final response:")
            print(final_text)    
            break

if __name__ == "__main__":
    main()