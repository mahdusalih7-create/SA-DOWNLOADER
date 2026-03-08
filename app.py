from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        url = request.form.get("url")
        download_type = request.form.get("type")

        file_id = str(uuid.uuid4())
        filename = os.path.join(DOWNLOAD_FOLDER, file_id)

        try:

            ydl_opts = {
                "format": "best",
                "outtmpl": filename + ".%(ext)s",
                "quiet": True,
                "noplaylist": True,
                "nocheckcertificate": True,
                "geo_bypass": True,
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
                    "Accept-Language": "en-US,en;q=0.9"
                },
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android"]
                    }
                }
            }

            # تحميل صوت
            if download_type == "audio":
                ydl_opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                if download_type == "audio":
                    ext = "mp3"
                else:
                    ext = info.get("ext", "mp4")

            file_path = filename + "." + ext

            return send_file(file_path, as_attachment=True)

        except Exception as e:
            return f"حدث خطأ أثناء التحميل: {str(e)}"

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
