# from agents import Agent, Runner
# from main import config
# agent = Agent(
# name = 'General Agent',
# instructions = "You are a helpful assistant. Your task is to help to user with their queries."
# )
# result = Runner.run_sync(
# agent,
# # "What is the difference between AI and Machine Learning? make it concise",
# # "What is the current time?",
# "What is the conversion of USD to PKR?",

# run_config = config
# )
# print(result.final_output)





from agents import Agent, Runner, function_tool, RunContextWrapper
import asyncio

from connection import config
from dataclasses import dataclass


@dataclass
class UserInfo:
    name: str
    uid: int


@function_tool
async def fetch_user_age(
    wrapper: RunContextWrapper[UserInfo],
) -> str:
    return f"User {wrapper.context.name} is 25 years old."  # this is Local context


async def main():
    user_info = UserInfo(
        name="Muhammad Adeel",
        uid=66,
    )

    agent = Agent[UserInfo](
        name="Assistant",
        # instructions="use the `fetch_user_age` tool to get the user's age.",
        tools=[fetch_user_age],
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
        run_config=config,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())