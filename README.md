# LLM-SWE
CS 4501 LLMs and Software Engineering

This course explores the transformative impact of Large Language Models (LLMs) on modern software engineering. Students will learn to leverage LLMs to enhance their productivity across the software development lifecycle, from coding and testing to debugging and maintenance. We will also practice how to be cognizant of the ethical and safety implications of using LLMs in software development.

## Usage of .env
The `.env` file is used to store sensitive information such as API keys without hard-coding them directly into the source code.

Create a `.env` file inside the `llm-api` folder and add your Gemini API key:

```env
GEMINI_API_KEY="your_api_key_here"
```
Install the required packages:

```bash
py -m pip install python-dotenv google-genai
```

Load the environment variable in Python:

```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Make sure the `.env` file is not committed to GitHub. Add the following line to `.gitignore`:

```gitignore
llm-api/.env
```

You can verify that `.env` is not being tracked by Git with:

```bash
git ls-files | grep .env
```

If no output appears, the file is not being tracked.

Never commit or share API keys publicly. If an API key is accidentally committed, revoke or rotate the key and replace it in your local `.env` file.