from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

# مسار ffmpeg المرفق داخل المشروع
ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg")

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        mode = request.form["type"]
        temp_dir = tempfile.gettempdir()

        try:
            if mode == "video":
                filename = os.path.join(temp_dir, "video.mp4")
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "merge_output_format": "mp4",
                    "outtmpl": filename,
                    "ffmpeg_location": ffmpeg_path
                }
            else:
                filename = os.path.join(temp_dir, "audio.mp3")
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": filename,
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                        "ffmpeg_location": ffmpeg_path
                    }]
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(filename, as_attachment=True)

        except Exception as e:
            return f"حدث خطأ أثناء التحميل: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
