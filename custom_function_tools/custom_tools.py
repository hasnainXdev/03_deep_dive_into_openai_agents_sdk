import os
import dotenv

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
    RunContextWrapper,
    FunctionTool
)
from typing import Any
from openai import AsyncOpenAI
from pydantic import BaseModel

dotenv.load_dotenv()

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


def kuch_kar(data: str) -> str:
    return "kardia kuch"


class FunctionArgs(BaseModel):
    username:str
    age: int
    
async def run_function(ctx:RunContextWrapper[Any], args:str)-> str:
    parsed = FunctionArgs.model_validate_json(args)
    return kuch_kar(data=f"{parsed.username} is {parsed.age} year old")


tool = FunctionTool(
    name="process_user",
    description="processs extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function
)



agent = Agent(
    name="Assistant", 
    instructions="you are an expert assistant who answer user queries", 
    model=model,
    tools=[tool]
)


result = Runner.run_sync(agent, input="give me user data")


print(agent.tools)
