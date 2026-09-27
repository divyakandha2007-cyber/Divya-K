from pydantic import BaseModel, Field, field_validator


class PanelOutline(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str


class OutlineResponse(BaseModel):
    panels: list[PanelOutline] = Field(min_length=5, max_length=5)


class PanelStory(BaseModel):
    panel_number: int
    caption: str
    narration: str
    dialogue: str


class StoryResponse(BaseModel):
    panels: list[PanelStory] = Field(min_length=5, max_length=5)


class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=1000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=100)
    tone: str = Field(min_length=1, max_length=50)
    art_style: str = Field(min_length=1, max_length=80)

    @field_validator("*")
    @classmethod
    def strip_values(cls, value):
        if isinstance(value, str):
            value = value.strip()

            if not value:
                raise ValueError("Field cannot be empty.")

        return value


class TestImageRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=1000)