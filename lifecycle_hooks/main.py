import os
import asyncio
import dotenv
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
    RunContextWrapper,
)
from agents.lifecycle import AgentHooks, RunHooks

from openai import AsyncOpenAI

# Load environment variables
dotenv.load_dotenv()

# Set Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Disable tracing for simplicity
set_tracing_disabled(disabled=True)

# Configure external Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define the Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=external_client
)


# Define a custom hook for lifecycle events
class MyAgentHooks(AgentHooks):
    async def on_start(self, context: RunContextWrapper, agent: Agent):
        print("called on_start")
        print(f"Agent {agent.name} is starting to process your request!")
    async def on_end(self, context: RunContextWrapper, agent: Agent):
        print("called on_start")
        print(f"Agent {agent.name} is ended!")


# Create an Agent
agent = Agent(
    name="MathAssistant",
    instructions="You are a math assistant. Use the provided tools to perform calculations and explain results clearly.",
    model=model,
    hooks=MyAgentHooks(),
)


result = Runner.run_sync(agent, input="2 + 2")
print(result.final_output)
