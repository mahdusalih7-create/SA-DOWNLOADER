from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":

        url = request.form["url"]
        mode = request.form["type"]

        try:

            if mode == "video":

                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "merge_output_format": "mp4",
                    "outtmpl": "video.%(ext)s"
                }

                filename = "video.mp4"

            else:

                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": "audio.%(ext)s",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }]
                }

                filename = "audio.mp3"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(filename, as_attachment=True)

        except:
            return "حدث خطأ أثناء التحميل"

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
