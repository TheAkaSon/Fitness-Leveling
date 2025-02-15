document.getElementById("videoForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let url = document.getElementById("videoUrl").value;

    if (!url.includes("youtube.com") && !url.includes("youtu.be")) {
        showError("URL invalide !");
        return;
    }

    document.getElementById("loading").classList.remove("d-none");

    try {
        const videoBlob = await downloadVideo(url);
        saveVideo(videoBlob);
    } catch (error) {
        showError("Erreur lors du téléchargement !");
    } finally {
        document.getElementById("loading").classList.add("d-none");
    }
});

async function downloadVideo(videoUrl) {
    return new Promise((resolve, reject) => {
        yt_dlp.download(videoUrl, { format: "best", noMetadata: true }, (videoBlob) => {
            if (videoBlob) resolve(videoBlob);
            else reject(new Error("Téléchargement échoué"));
        });
    });
}

function saveVideo(videoBlob) {
    let a = document.createElement("a");
    a.href = URL.createObjectURL(videoBlob);
    a.download = "video_sans_licence.mp4";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function showError(message) {
    let errorDiv = document.getElementById("error");
    errorDiv.textContent = message;
    errorDiv.classList.remove("d-none");
}
