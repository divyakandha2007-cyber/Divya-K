from google import genai
from google.genai import types

from ..config import settings
from ..schemas import OutlineResponse


def _client():
    if (
        not settings.gemini_api_key
        or settings.gemini_api_key == "your_gemini_api_key_here"
    ):
        raise RuntimeError(
            "GEMINI_API_KEY is missing or still uses the placeholder value. "
            "Add a valid key to your .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> list[dict]:

    prompt = f"""
Create exactly 5 connected comic panels.

User story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Requirements:

1. Create exactly five panels.
2. Keep the same main character throughout the story.
3. Make the story have a clear beginning, development,
   climax, and ending.
4. Each panel must have:
   - panel_number
   - title
   - scene_description
   - image_prompt
5. The image_prompt must describe the visual scene clearly.
6. Preserve character identity and setting between panels.
7. Use the requested art style.
8. Do not put speech bubbles or written text inside images.
9. Make the five panels feel like one continuous comic.
"""

    client = _client()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=OutlineResponse,
            temperature=0.9,
        ),
    )

    parsed = response.parsed

    if parsed is None:
        parsed = OutlineResponse.model_validate_json(
            response.text
        )

    return [
        panel.model_dump()
        for panel in parsed.panels
    ]