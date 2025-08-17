from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)


agent = Agent(
    name="Assistant",
    instructions="you are an AI assistant that helps with python programming cocepts shortly.",  # this is the system prompt for the agent that runs inside your code, the enable yoy to do anything you want, use case: for example -> you can pass code to the agent and it will review it and return the result...
    model=model,
)

result = Runner.run_sync(
    agent,
    input="what is recursion?",
)

print(f"{result.final_output}")
