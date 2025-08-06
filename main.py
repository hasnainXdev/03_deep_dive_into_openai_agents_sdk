import os
import dotenv

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    RunConfig,
    function_tool,
    set_tracing_disabled,
    ModelSettings,
    AsyncOpenAI,
    enable_verbose_stdout_logging,
)
from agents.agent import StopAtTools

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

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)


@function_tool()
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    print("add was called")
    return a + b - 5


@function_tool()
def human_review():
    """Human in the loop interface."""
    print("human_review called")
    return "human in the loop called."


agent = Agent(
    name="Personal Assistant",
    instructions="You are a personal assistant. Answer questions to the best of your ability",
    tools=[add, human_review],
    
)

result = Runner.run_sync(
    agent,
    input="What is 2 plus 2? after result as",
)


print(result.final_output)
