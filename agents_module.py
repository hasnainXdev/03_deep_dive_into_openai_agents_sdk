import os
import asyncio
import dotenv
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    RunConfig,
    function_tool,
    set_tracing_disabled,
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


# Define a simple tool
def square_number(number: int) -> int:
    """Calculates the square of a given number."""
    return number * number


square_tool = function_tool(square_number)


# Define a custom hook for lifecycle events
class MyAgentHooks(AgentHooks):
    async def on_agent_start(self, context, agent):
        print(f"Agent {agent.name} is starting to process your request!")


# Create an Agent
agent = Agent(
    name="MathAssistant",
    instructions="You are a math assistant. Use the provided tools to perform calculations and explain results clearly.",
    model=model,
    tools=[square_tool],
    hooks=[MyAgentHooks],
)


# Run the agent
async def run_math_assistant():
    result = await Runner.run(
        agent, input="Calculate the square of 5 and explain the result."
    )
    print("Agent Response:", result.final_output)


# Execute the async function
if __name__ == "__main__":
    asyncio.run(run_math_assistant())
