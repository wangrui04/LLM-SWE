# LLM-SWE
CS 4501 LLMs and Software Engineering

This course explores the transformative impact of Large Language Models (LLMs) on modern software engineering. Students will learn to leverage LLMs to enhance their productivity across the software development lifecycle, from coding and testing to debugging and maintenance. We will also practice how to be cognizant of the ethical and safety implications of using LLMs in software development.

## Repository Structure

```text
LLM-SWE/
├── llm-api/
│   ├── .env              # Local environment variables / API keys (untracked)
│   └── code.py           # Gemini-powered debugging script
├── .gitignore            # Git ignore rules (protecting .env)
├── LICENSE
├── README.md
└── requirements.txt      # Project dependencies
```

## AI Code Debugger (`llm-api`)

The `llm-api` module implements an automated debugging assistant using Google's Gemini API (`gemini-3.6-flash`).

### Function: `debug_me`
Located in `llm-api/code.py`:

```python
def debug_me(language: str, code_snippet: str, error_log: str) -> str
```

- **Parameters**:
  - `language` (*str*): The programming language of the target code (e.g., `"Python"`).
  - `code_snippet` (*str*): The code snippet experiencing the bug.
  - `error_log` (*str*): The error message, exception, or runtime traceback.
- **Returns**: A diagnostic report from Gemini identifying the root cause and providing a code fix.

---

## Setup & Installation

### 1. Install Dependencies
Ensure Python 3.10+ is installed. Install the project dependencies from the root `requirements.txt`:

```bash
py -m pip install -r requirements.txt
# or: pip install -r requirements.txt
```

### 2. Environment Configuration (.env)
The `.env` file is used to store sensitive information such as API keys without hard-coding them directly into the source code.

1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
2. Create a `.env` file inside the `llm-api` folder:

```env
GEMINI_API_KEY="your_api_key_here"
```

In Python, the API key is loaded via `python-dotenv`:

```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

### 3. Security & Git Configuration
Make sure the `.env` file is not committed to GitHub. Add the following line to `.gitignore`:

```gitignore
llm-api/.env
```

Verify that `.env` is not being tracked by Git:

- **Bash / macOS / Linux:**
  ```bash
  git ls-files | grep .env
  ```
- **PowerShell (Windows):**
  ```powershell
  git ls-files | Select-String .env
  ```

If no output appears, the file is not being tracked.

> **Important:** Never commit or share API keys publicly. If an API key is accidentally committed, revoke or rotate the key in Google AI Studio and replace it in your local `.env` file.

---

## Running the Code

Run the sample debugger directly from the `llm-api` directory:

```bash
cd llm-api
py code.py
# or: python code.py
```

### Example Usage in Code

```python
from code import debug_me

result = debug_me(
    language="Python",
    code_snippet="print(10/0)",
    error_log="ZeroDivisionError: division by zero",
)

print(result)
```