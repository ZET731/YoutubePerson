from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def descargar_video_audio(url, tipo):
    try:
        filename = "audio.mp3" if tipo == "audio" else "video.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {}
        if tipo == "audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': filepath,
            }
        elif tipo == "video":
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                }],
                'outtmpl': filepath,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return filepath
    except Exception as e:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        tipo = request.form["tipo"]
        archivo = descargar_video_audio(url, tipo)
        if archivo:
            return f'Descarga completada. <a href="/descargar?archivo={archivo}">Descargar aquí</a>'
        else:
            return "Ocurrió un error en la descarga."
    return render_template("index.html")

@app.route("/descargar")
def descargar():
    archivo = request.args.get("archivo")
    if archivo and os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    return "Archivo no encontrado."

if __name__ == "__main__":
    app.run(debug=True)
