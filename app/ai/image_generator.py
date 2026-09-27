import re
from pathlib import Path
from uuid import uuid4

from PIL import Image

from ..config import settings


BASE_DIR = Path(__file__).resolve().parent.parent

PANEL_DIR = (
    BASE_DIR
    / "static"
    / "panels"
)

PANEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def _safe_name(text: str) -> str:

    name = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "-",
        text
    )

    name = name.strip("-")

    return name[:50] or "panel"


def _huggingface_image(
    prompt: str
) -> Image.Image:

    if (
        not settings.hf_token
        or settings.hf_token == "your_huggingface_token_here"
    ):
        raise RuntimeError(
            "HF_TOKEN is missing or still uses the placeholder value. "
            "Add a valid token to your .env file."
        )

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        provider=settings.image_provider,
        api_key=settings.hf_token,
    )

    image = client.text_to_image(
        prompt=prompt,
        model=settings.image_model,
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=settings.image_steps,
    )

    return image


def _local_diffusers_image(
    prompt: str
) -> Image.Image:

    import torch

    from diffusers import DiffusionPipeline

    dtype = (
        torch.float16
        if torch.cuda.is_available()
        else torch.float32
    )

    pipe = DiffusionPipeline.from_pretrained(
        settings.image_model,
        torch_dtype=dtype,
    )

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    pipe = pipe.to(device)

    result = pipe(
        prompt,
        width=settings.image_width,
        height=settings.image_height,
    )

    return result.images[0]


def generate_image(
    prompt: str,
    panel_number: int
) -> str:

    final_prompt = f"""
{prompt}

High-quality illustrated comic panel,
coherent character design,
consistent character appearance,
strong composition,
expressive faces,
clean line art,
cinematic lighting,
detailed environment,
professional comic illustration,
no text,
no watermark,
no logo.
"""

    if settings.image_backend.lower() == "local":

        image = _local_diffusers_image(
            final_prompt
        )

    else:

        image = _huggingface_image(
            final_prompt
        )

    filename = (
        f"{panel_number:02d}-"
        f"{_safe_name(prompt)}-"
        f"{uuid4().hex[:8]}.png"
    )

    path = PANEL_DIR / filename

    image.save(
        path,
        "PNG"
    )

    return f"/static/panels/{filename}"