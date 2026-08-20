# import chainlit as cl


# @cl.on_message
# async def main(message: cl.Message):
#     response = f"Received: {message.content}"

#     await cl.Message(
#         content=response
#     ).send()








# import os

# from dotenv import load_dotenv
# from typing import cast
# import chainlit as cl

# from agents import (
#     Agent,
#     Runner,
#     AsyncOpenAI,
#     OpenAIChatCompletionsModel,
#     OpenAIProvider,
# )
# from agents.run import RunConfig

# load_dotenv(override=True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # check if the API key is present; if not, raise an error
# if not gemini_api_key:
#     raise ValueError(
#         "GEMINI_API_KEY is not set. Please ensure it is defined in your .env "
#         "file."
#     )


# @cl.on_chat_start
# async def start():
#     # Reference: https://ai.google.dev/gemini-api/docs

#     # Instantiate the OpenAI client
#     external_client = AsyncOpenAI(
#         api_key=gemini_api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

#     # Instantiate the Model instance for chat completions
#     model_instance = OpenAIChatCompletionsModel(
#         model="gemini-flash-latest",  # Use the verified model name
#         openai_client=external_client,
#     )

#     # Instantiate the ModelProvider
#     provider_instance = OpenAIProvider(
#         openai_client=external_client  # Pass the client to the provider
#     )

#     config = RunConfig(
#         model=model_instance,  # Pass the Model instance
#         model_provider=provider_instance,  # Pass the ModelProvider instance
#         tracing_disabled=True,
#     )

#     cl.user_session.set("chat_history", [])
#     cl.user_session.set("config", config)

#     agent: Agent = Agent(
#         name="Assistant",
#         instructions="You are a helpful assistant.",
#         model=model_instance,  # Pass the Model instance to the Agent
#     )

#     cl.user_session.set("agent", agent)

#     await cl.Message(
#         content="Welcome to the SMIU AI Assistant! How can I help you today?"
#     ).send()


# @cl.on_message
# async def main(message: cl.Message):
#     msg = cl.Message(content="Thinking...")

#     await msg.send()

#     agent: Agent = cast(
#         Agent,
#         cl.user_session.get("agent"),
#     )

#     config: RunConfig = cast(
#         RunConfig,
#         cl.user_session.get("config"),
#     )

#     history = cl.user_session.get("chat_history") or []

#     history.append(
#         {
#             "role": "user",
#             "content": message.content,
#         }
#     )

#     try:
#         print(
#             "\n[CALLING_AGENT_WITH_CONTEXT]\n",
#             history,
#             "\n",
#         )

#         result = await Runner.run(
#             starting_agent=agent,
#             input=history,
#             run_config=config,
#         )

#         response_content = result.final_output

#         msg.content = response_content
#         await msg.update()

#         cl.user_session.set(
#             "chat_history",
#             result.to_input_list(),
#         )

#         print(f"User: {message.content}")
#         print(f"Assistant: {response_content}")

#     except Exception as e:
#         msg.content = f"Error: {str(e)}"
#         await msg.update()

#         print(f"Error: {str(e)}")





# from agents import (
#     Agent,
#     AsyncOpenAI,
#     OpenAIChatCompletionsModel,
#     RunConfig,
#     Runner,
# )

# from dotenv import load_dotenv
# import os

# load_dotenv(override=True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # check if the API key is present; if not, raise an error
# if not gemini_api_key:
#     raise ValueError(
#         "GEMINI_API_KEY is not set. Please ensure it is defined in your .env "
#         "file."
#     )

# # Reference: https://ai.google.dev/gemini-api/docs

# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-flash-latest",
#     openai_client=external_client,
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True,
# )



from agents import Runner
import asyncio

from connection import config
from handoff import triage_agent


async def main():
    result = await Runner.run(
        triage_agent,
        "My order arrived 10 days late. I want a refund.",
        run_config=config,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())