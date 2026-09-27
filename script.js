// ========================================
// COMICCRAFT - JAVASCRIPT
// ========================================


// Get HTML elements

const form =
    document.getElementById("comicForm");

const comicGrid =
    document.getElementById("comicGrid");

const resultInfo =
    document.getElementById("resultInfo");


// ========================================
// 5 COMIC PANELS
// ========================================

const panels = [

    {
        title: "A New Adventure",

        scene:
        "sets off from his village with a big dream in his heart.",

        caption:
        "The journey begins...",

        narration:
        "He waved goodbye to his friends and started his adventure, full of hope and excitement.",

        imagePrompt:
        "A cute orange fox with a small backpack standing at the edge of a forest during sunrise, beautiful mountains in the background, warm golden sunlight, colorful comic book illustration."
    },


    {
        title: "Into the Unknown",

        scene:
        "enters the mysterious forest. Strange sounds and hidden paths make him curious.",

        caption:
        "The forest holds many secrets...",

        narration:
        "Despite his fear, he kept moving forward, following the faint path.",

        imagePrompt:
        "A cute orange fox with a small backpack walking deep inside a mysterious green forest, tall trees, sunlight through leaves, adventurous atmosphere, colorful comic book illustration."
    },


    {
        title: "The Hidden Secret",

        scene:
        "discovers a glowing magical stone hidden between the trees.",

        caption:
        "Something magical was waiting...",

        narration:
        "He slowly reached out and touched the glowing stone. A warm light filled the forest.",

        imagePrompt:
        "A cute orange fox discovering a glowing magical blue stone between ancient trees, magical light illuminating the fox, fantasy forest, colorful comic book illustration."
    },


    {
        title: "The Great Challenge",

        scene:
        "faces a huge wolf that blocks the path.",

        caption:
        "Courage is stronger than fear.",

        narration:
        "He did not run. He stayed calm, thought carefully, and found a clever way forward.",

        imagePrompt:
        "A brave orange fox with a backpack facing a large gray wolf in a mysterious forest, dramatic action scene, expressive characters, colorful comic book illustration."
    },


    {
        title: "A New Beginning",

        scene:
        "reaches a beautiful hidden valley filled with waterfalls and flowers.",

        caption:
        "Every adventure leads to a new beginning.",

        narration:
        "He smiled, knowing that the best part of his journey was still ahead.",

        imagePrompt:
        "A happy orange fox with a backpack standing on a hill looking at a beautiful hidden valley with waterfalls, flowers and mountains, golden sunset, magical adventure ending, colorful comic book illustration."
    }

];


// ========================================
// GENERATE COMIC
// ========================================

form.addEventListener("submit", function(event) {

    // Stop page refresh
    event.preventDefault();


    // Get form values

    const character =
        document.getElementById("character").value || "Arun";


    const setting =
        document.getElementById("setting").value;


    const tone =
        document.getElementById("tone").value;


    const artStyle =
        document.getElementById("artStyle").value;


    const story =
        document.getElementById("story").value;


    // Get uploaded images

    const imageInput =
        document.getElementById("panelImages");

    const uploadedImages =
        imageInput.files;


    // ========================================
    // CHECK IMAGE COUNT
    // ========================================

    if (uploadedImages.length === 0) {

        alert(
            "Please upload at least one comic image."
        );

        return;
    }


    // ========================================
    // RESULT INFORMATION
    // ========================================

    resultInfo.textContent =
        character +
        " • " +
        setting +
        " • " +
        tone +
        " • " +
        artStyle;


    // Remove old panels

    comicGrid.innerHTML = "";


    // ========================================
    // CREATE 5 PANELS
    // ========================================

    panels.forEach(function(panel, index) {


        // Create panel

        const comic =
            document.createElement("article");


        comic.className =
            "comic-panel";


        // ========================================
        // IMAGE
        // ========================================

        let imageHTML;


        if (uploadedImages[index]) {

            const imageURL =
                URL.createObjectURL(
                    uploadedImages[index]
                );


            imageHTML = `

                <img
                    src="${imageURL}"
                    alt="Comic Panel ${index + 1}"
                >

            `;

        }

        else {

            imageHTML = `

                <div class="no-image">

                    🖼️ Image not uploaded

                </div>

            `;

        }


        // ========================================
        // PANEL HTML
        // ========================================

        comic.innerHTML = `

            <h3>
                Panel ${index + 1}:
                ${panel.title}
            </h3>


            ${imageHTML}


            <p class="scene">

                <b>SCENE:</b>

                ${character}
                ${panel.scene}

            </p>


            <p>

                <b>CAPTION:</b>

                "${panel.caption}"

            </p>


            <p>

                <b>NARRATION:</b>

                "${
                    index === 0
                    ? story
                    : panel.narration
                }"

            </p>


            <p>

                <b>IMAGE PROMPT:</b>

                ${panel.imagePrompt}

            </p>

        `;


        // Add panel

        comicGrid.appendChild(comic);

    });


    // ========================================
    // SCROLL TO RESULT
    // ========================================

    document
        .getElementById("result")
        .scrollIntoView({
            behavior: "smooth"
        });

});


// ========================================
// DOWNLOAD / PRINT
// ========================================

function downloadComic() {

    window.print();

}