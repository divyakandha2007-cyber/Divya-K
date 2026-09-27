from google import genai
from google.genai import types

from ..config import settings
from ..schemas import StoryResponse


def generate_story(
    outline: list[dict],
    character_name: str,
    tone: str,
) -> list[dict]:

    if (
        not settings.gemini_api_key
        or settings.gemini_api_key == "your_gemini_api_key_here"
    ):
        raise RuntimeError(
            "GEMINI_API_KEY is missing or still uses the placeholder value. "
            "Add a valid key to your .env file."
        )

    prompt = f"""
Expand the following five-panel comic outline into
a polished comic story.

Main character:
{character_name}

Tone:
{tone}

Comic outline:
{outline}

For every panel create:

1. caption
   - A short description of the environment or atmosphere.

2. narration
   - One to three sentences describing the action,
     emotion, or story progression.

3. dialogue
   - Natural dialogue spoken by characters.
   - If dialogue is not necessary, return an empty string.

Requirements:

- Keep the story continuous.
- Keep character names consistent.
- Do not create additional panels.
- Do not change the main story.
- Keep the requested tone.
"""

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StoryResponse,
            temperature=0.85,
        ),
    )

    parsed = response.parsed

    if parsed is None:
        parsed = StoryResponse.model_validate_json(
            response.text
        )

    return [
        panel.model_dump()
        for panel in parsed.panels
    ]