from pathlib import Path
from uuid import uuid4

from fpdf import FPDF
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent.parent

EXPORT_DIR = (
    BASE_DIR
    / "static"
    / "exports"
)

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def _pdf_text(value: str) -> str:

    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "-",
        "–": "-",
        "…": "...",
        "•": "*",
        "✨": "*",
        "✓": "OK",
    }

    text = str(value or "")

    for old, new in replacements.items():
        text = text.replace(
            old,
            new
        )

    return (
        text
        .encode(
            "latin-1",
            "replace"
        )
        .decode("latin-1")
    )


def _image_path(
    web_path: str
) -> Path:

    relative = web_path.removeprefix(
        "/static/"
    )

    return (
        BASE_DIR
        / "static"
        / relative
    )


def save_pdf(
    layout: list[dict],
    title: str = "ComicCraft Comic",
) -> str:

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.multi_cell(
            0,
            10,
            _pdf_text(
                f"Panel "
                f"{panel['panel_number']}: "
                f"{panel['title']}"
            )
        )

        pdf.ln(2)

        path = _image_path(
            panel["image_path"]
        )

        if path.exists():

            with Image.open(path) as img:

                width, height = img.size

                max_width = 180
                max_height = 115

                ratio = min(
                    max_width / width,
                    max_height / height
                )

                image_width = width * ratio
                image_height = height * ratio

            x = (
                210 - image_width
            ) / 2

            pdf.image(
                str(path),
                x=x,
                y=pdf.get_y(),
                w=image_width,
                h=image_height,
            )

            pdf.ln(
                image_height + 5
            )

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        pdf.multi_cell(
            0,
            6,
            _pdf_text(
                panel[
                    "scene_description"
                ]
            )
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            6,
            "Caption"
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            _pdf_text(
                panel["caption"]
            )
        )

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            6,
            "Narration"
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            _pdf_text(
                panel["narration"]
            )
        )

        if panel.get("dialogue"):

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                6,
                "Dialogue"
            )

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            pdf.multi_cell(
                0,
                6,
                _pdf_text(
                    panel["dialogue"]
                )
            )

    filename = (
        f"comic-"
        f"{uuid4().hex[:10]}"
        f".pdf"
    )

    output = (
        EXPORT_DIR
        / filename
    )

    pdf.output(
        str(output)
    )

    return (
        f"/static/exports/"
        f"{filename}"
    )