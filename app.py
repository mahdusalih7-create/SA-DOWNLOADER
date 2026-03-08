from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        type_download = request.form["type"]

        file_id = str(uuid.uuid4())
        filename = os.path.join(DOWNLOAD_FOLDER, file_id)

        try:
            ydl_opts = {
                "format": "bv*+ba/b",
                "outtmpl": filename + ".%(ext)s",
                "quiet": True,
                "http_headers": {
                    "User-Agent": "Mozilla/5.0"
                }
            }

            if type_download == "audio":
                ydl_opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                ext = "mp3" if type_download == "audio" else info["ext"]

            file_path = filename + "." + ext

            return send_file(file_path, as_attachment=True)

        except Exception as e:
            return f"حدث خطأ أثناء التحميل: {str(e)}"

    return render_template("index.html")

app.run(host="0.0.0.0", port=3000)
