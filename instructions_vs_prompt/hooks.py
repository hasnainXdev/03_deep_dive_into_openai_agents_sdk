from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    ModelSettings,
    AgentHooks,
    RunContextWrapper,
)
from typing import Any
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


class myAgentHook(AgentHooks):
    async def on_start(self, ctx: RunContextWrapper[None], agent: Agent):
        print(f"{agent.name} agent is started and ready to assist")

    async def on_end(self, ctx: RunContextWrapper, agent: Agent, output: Any):
        print(f"{agent.name} agent is ended")


agent = Agent(
    name="Assistant",
    instructions="you are an AI assistant that helps with python programming cocepts shortly.",  # this is the system prompt for the agent that runs inside your code, the enable you to do anything you want, use case: for example -> you can pass code to the agent and it will review it and return the result...
    model=model,
    hooks=myAgentHook(),
)

result = Runner.run_sync(
    agent,
    input="what is recursion?",
)

print(f"{result.final_output}")
