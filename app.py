from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import shutil

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_video_info(url):
    """Récupère les infos d'une vidéo YouTube automatiquement."""
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title", "Inconnu"),
            "author": info.get("uploader", "Inconnu"),
            "duration": info.get("duration", "Inconnu"),
            "views": info.get("view_count", "Inconnu"),
            "likes": info.get("like_count", "Inconnu"),
            "subscribers": "Inconnu",
            "license": info.get("license", "Standard YouTube License"),
            "thumbnail": info.get("thumbnail", ""),
        }

def remove_metadata(file_path):
    """Supprime les métadonnées du fichier vidéo/audio."""
    new_file = file_path.replace(".", "_nometa.")
    os.system(f'ffmpeg -i "{file_path}" -map_metadata -1 -c:v copy -c:a copy "{new_file}" -y')
    os.remove(file_path)  # Supprime l'original
    os.rename(new_file, file_path)  # Renomme le fichier nettoyé

def download_video(url, remove_copyright=False, audio_only=False):
    """Télécharge la vidéo avec options."""
    options = {
        'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        'format': 'bestaudio/best' if audio_only else 'best',
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    if remove_copyright:
        remove_metadata(filename)  # Nettoie les métadonnées du fichier

    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        remove_copyright = request.form.get("remove_copyright") == "on"
        audio_only = request.form.get("audio_only") == "on"

        if not url:
            return render_template("index.html", error="Veuillez entrer une URL YouTube.")

        video_info = get_video_info(url)
        filename = download_video(url, remove_copyright, audio_only)
        return send_file(filename, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
