# Import the required libraries.
import asyncio
import os
from typing import Any, Annotated
from genai_session.session import GenAISession 
from google import genai
from dotenv import load_dotenv


# Load the Google API Key from the .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")


# Create a single, reusable client instance using your API key.
# This client object will be used for all interactions with the Google API.
client = genai.Client(api_key=api_key)

#Initialize the connection to YOUR agent framework server.
session = GenAISession(
    jwt_token="JWT token",          # replace with your token
    ws_url="ws://localhost:8080/ws"
)


# --- THE AGENT TOOL DEFINITION  ---
# The `@session.bind` decorator registers this Python function as a tool
# that the master agent can see and decide to use.

@session.bind(name="translate_text", description="Translate text from one language to another.")
async def translate_text(
        agent_context, # Provided by the GenAISession framework
        text: Annotated[str, "The text to translate."],
        source_language: Annotated[str, "The source language of the text (e.g., 'English')."],
        target_language: Annotated[str, "The language to translate the text into (e.g., 'Spanish')."]
) -> dict[str, Any]:
    """
    It is designed to handle idiomatic expressions and produce fluent, natural phrasing.
    """
    agent_context.logger.info(f"Tool 'gemini_translator' invoked. Translating '{text}' from {source_language} to {target_language}.")
    
    try:
        # Define the model to use.
        model_name = 'gemini-2.5-flash'

        # Create the precise instructions for the LLM.
        prompt = f"""
        As an expert translator, translate the following text from {source_language} to {target_language}.
        Your translation must be natural and fluent, accurately handling any idioms or cultural nuances.
        Preserve the original tone and intent.

        Text to translate: "{text}"

        Provide ONLY the translated text in your response, with no extra explanations.
        """

        # Perform the asynchronous API call to Google's servers.
        response = await client.aio.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        translated_text = response.text.strip()
        agent_context.logger.info(f"Translation successful: '{translated_text}'")

        # Return the result in the required dictionary format.
        return {"translated_text": translated_text}

    except Exception as e:
        # If anything goes wrong, log the error and return an error message.
        agent_context.logger.error(f"Gemini translation failed: {e}", exc_info=True)
        return {"error": f"Translation failed due to an API error: {e}"}



# --- AGENT EXECUTION LOOP  ---

async def main():
    """Connects to the agent server and waits for jobs."""
    print("Gemini Translator Agent (using new google-genai SDK) is running.")
    print("Waiting for the orchestrator to assign translation tasks...")
    await session.process_events()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")