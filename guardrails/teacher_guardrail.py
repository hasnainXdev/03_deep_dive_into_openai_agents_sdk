import os
import dotenv

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    RunConfig,
    set_tracing_disabled,
    AsyncOpenAI,
    input_guardrail,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    GuardrailFunctionOutput,
)
import asyncio

from agents.agent import StopAtTools
from pydantic import BaseModel

dotenv.load_dotenv()

# enable_verbose_stdout_logging()

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


class CheckForStudent(BaseModel):
    reasoning: str
    is_student_checking_attendees: bool


teacher_agent = Agent(
    name="Teacher Agent",
    instructions="You are an expert teacher agent. You will review that the student is not allowed to check other student attendees if they do return True",
    output_type=CheckForStudent,
)


@input_guardrail()
async def check_for_student(
    ctx, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(teacher_agent, input, run_config=config, context=ctx)
    print(result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_student_checking_attendees,
    )


security_agent = Agent(
    name="Security Agent",
    instructions="You are a security agent. You will check all students that they does'nt checking other students attendees",
    input_guardrails=[check_for_student],
)


async def main():
    try:
        result = await Runner.run(
            security_agent,
            run_config=config,
            input="I'm checking other students attendees",
        )

        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail tripped - you are not admited!")


if __name__ == "__main__":

    asyncio.run(main())
