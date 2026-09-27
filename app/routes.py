from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from .schemas import (
    PromptRequest,
    TestImageRequest,
)

from .ai.gemini_flash import (
    generate_outline,
)

from .ai.gemini_pro import (
    generate_story,
)

from .ai.image_generator import (
    generate_image,
)

from .layout_builder import (
    build_comic_layout,
)

from .exporters import (
    save_pdf,
)


router = APIRouter()


@router.get("/")
async def home(
    request: Request
):

    return request.app.state.templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        },
    )


def _generate(
    payload: PromptRequest
):

    # STEP 1
    # Generate five-panel outline.

    outline = generate_outline(
        payload.story_prompt,
        payload.character_name,
        payload.setting,
        payload.tone,
        payload.art_style,
    )

    # STEP 2
    # Generate narration/dialogue.

    story = generate_story(
        outline,
        payload.character_name,
        payload.tone,
    )

    # STEP 3
    # Generate images.

    image_paths = []

    for panel in outline:

        image_path = generate_image(
            panel["image_prompt"],
            panel["panel_number"],
        )

        image_paths.append(
            image_path
        )

    # STEP 4
    # Build final layout.

    layout = build_comic_layout(
        outline,
        story,
        image_paths,
    )

    # STEP 5
    # Create PDF.

    pdf_path = save_pdf(
        layout,
        f"{payload.character_name}'s Comic",
    )

    return layout, pdf_path


@router.post("/generate")
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):

    try:

        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        layout, pdf_path = _generate(
            payload
        )

        return (
            request
            .app
            .state
            .templates
            .TemplateResponse(
                request,
                "comic_preview.html",
                {
                    "request": request,
                    "layout": layout,
                    "pdf_path": pdf_path,
                },
            )
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post(
    "/generate-comic/json"
)
async def generate_json(
    payload: PromptRequest
):

    try:

        layout, pdf_path = _generate(
            payload
        )

        return {
            "success": True,
            "layout": layout,
            "pdf_path": pdf_path,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/test-image")
async def test_image(
    payload: TestImageRequest
):

    try:

        path = generate_image(
            payload.prompt,
            1,
        )

        return {
            "success": True,
            "image_path": path,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "/export-success"
)
async def export_success(
    request: Request
):

    return (
        request
        .app
        .state
        .templates
        .TemplateResponse(
            request,
            "export_success.html",
            {
                "request": request
            },
        )
    )