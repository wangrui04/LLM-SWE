import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def debug_me(language: str, code_snippet: str, error_log: str) -> str:
    prompt = f"""
        You are an expert debugger.
        Help the user diagnose their {language} code.

        Code:
        {code_snippet}

        Error Log:
        {error_log}

        Instructions:
        Identify the root cause and provide a fix.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1024,
        ),
    )

    return response.text


if __name__ == "__main__":
    result = debug_me(
        language="Python",
        code_snippet="print(10/0)",
        error_log="ZeroDivisionError: division by zero",
    )

    print(result)