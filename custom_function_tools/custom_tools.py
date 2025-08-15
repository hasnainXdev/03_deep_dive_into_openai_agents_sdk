import os
import dotenv

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
    RunContextWrapper,
    FunctionTool,
    enable_verbose_stdout_logging,
    ModelSettings
)
from typing import Any
from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError

dotenv.load_dotenv()

# ====== SETUP ======
gemini_api_key = os.getenv("GEMINI_API_KEY")

# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=external_client
)


class FunctionArgs(BaseModel):
    username: str
    age: int


# ----- Tool Logic -----
def kuch_kar(data: str) -> str:
    print("called")
    return f"kardia kuch: {data}"


async def run_function(ctx: RunContextWrapper[FunctionArgs]) -> str:
    print("called")
    parsed = FunctionArgs.model_validate_json(ctx.context)
    return kuch_kar(data=f"{parsed.username} is {parsed.age} year old")


# @function_tool
# def run_function(ctx: RunContextWrapper[UserContext]) -> str:
#     print("called")
#     return f"{ctx.context.username} is {ctx.context.age} year old"

# ----- Tool Definition -----
user_data_tool = FunctionTool(
    name="process_user",
    description="process extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)

# ----- Agent -----
agent = Agent(
    name="Assistant",
    instructions=(
        """
        You are an expert assistant, only use tools never guess
        
        !important
        use the `user_data_tool` tool to get user age and username
        

        """
    ),
    model=model,
    tools=[user_data_tool],
    tool_use_behavior="stop_on_first_tool",
    model_settings=ModelSettings()
)

# ====== TEST RUN ======
# Case 1: Valid data
user_data_valid = FunctionArgs(username="arvind shrinvas", age=69)
result1 = Runner.run_sync(agent, input="give me user data", context=user_data_valid)
print("Valid data output:", result1.final_output)

# Case 2: Invalid data (age is missing)
# invalid_context = '{"username": "john"}'
# result2 = Runner.run_sync(agent, input="give me user data", context=invalid_context)
# print("Invalid data output:", result2.final_output)
