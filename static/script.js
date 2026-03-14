/* -------------------------
CARD FLIP FUNCTION
------------------------- */
function flipCard() {
    document.getElementById("flipCard").classList.toggle("flipped");
}

/* -------------------------
DECRYPT FUNCTION
------------------------- */
document.getElementById("decryptForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    let loader = document.getElementById("loader");
    let resultBox = document.getElementById("resultBox");
    let resultText = document.getElementById("resultText");

    // Show loader, hide previous result
    loader.style.display = "block";
    resultBox.style.display = "none";

    let formData = new FormData(this);

    try {
        let response = await fetch("/decrypt", {
            method: "POST",
            body: formData
        });

        let data = await response.json();

        // Hide loader, show result
        loader.style.display = "none";
        resultText.innerText = data.message;
        resultBox.style.display = "block";
        
    } catch (error) {
        // Simple error handling
        loader.style.display = "none";
        resultText.innerText = "Error decrypting the image. Please try again.";
        resultBox.style.display = "block";
    }
});

/* -------------------------
RELOAD PAGE AFTER ENCRYPT
------------------------- */
const encryptForm = document.querySelector('form[action="/encrypt"]');

if (encryptForm) {
    encryptForm.addEventListener("submit", function() {
        setTimeout(function() {
            window.location.reload();
        }, 3000);
    });
}