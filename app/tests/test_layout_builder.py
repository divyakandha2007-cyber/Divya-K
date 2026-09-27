from app.layout_builder import (
    build_comic_layout
)


def test_layout_pairs_panels_and_story():

    outline = [

        {
            "panel_number": 1,
            "title": "Start",
            "scene_description": "A",
            "image_prompt": "A",
        },

        {
            "panel_number": 2,
            "title": "Middle",
            "scene_description": "B",
            "image_prompt": "B",
        },

    ]


    story = [

        {
            "panel_number": 1,
            "caption": "C1",
            "narration": "N1",
            "dialogue": "D1",
        },

        {
            "panel_number": 2,
            "caption": "C2",
            "narration": "N2",
            "dialogue": "D2",
        },

    ]


    result = build_comic_layout(
        outline,
        story,
        [
            "/static/panels/1.png",
            "/static/panels/2.png",
        ],
    )


    assert result[0]["title"] == "Start"

    assert result[1]["dialogue"] == "D2"