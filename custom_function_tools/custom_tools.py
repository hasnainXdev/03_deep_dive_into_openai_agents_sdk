import os
import dotenv

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
)

from openai import AsyncOpenAI

dotenv.load_dotenv()

enable_verbose_stdout_logging()

# ====== SETUP ======
gemini_api_key = os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=external_client
)
