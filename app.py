import os
import shutil
import tempfile
from pathlib import Path
from threading import Lock
import yt_dlp
from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.wsgi import ClosingIterator
from downloader import SUPPORTED_FORMATS, download_media, normalize_video_url

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8192

DOWNLOAD_LOCK = Lock()

@app.after_request
def set_response_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if request.path == "/download":
        response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/docs")
def api_docs():
    return render_template("docs.html")

@app.get("/openapi.json")
def openapi_spec():
    return send_file(Path(__file__).with_name("openapi.json"), mimetype="application/json")

@app.post("/download")
def download():
    url = request.form.get("url", "").strip()
    formato = request.form.get("format", "").lower().strip()
    video_url = normalize_video_url(url)
    if not video_url or formato not in SUPPORTED_FORMATS:
        return "Informe um link de vídeo válido do YouTube e escolha MP3 ou MP4.", 400

    if not DOWNLOAD_LOCK.acquire(blocking=False):
        return "Já existe um download em andamento. Tente novamente depois.", 429

    directory = None
    handed_off = False
    try:
        directory = tempfile.mkdtemp(prefix="youtube-")
        file_path, filename = download_media(video_url, formato, directory)
        response = send_file(file_path, as_attachment=True, download_name=filename, conditional=False)

        def cleanup():
            shutil.rmtree(directory, ignore_errors=True)
            DOWNLOAD_LOCK.release()

        response.response = ClosingIterator(response.response, [cleanup])
        handed_off = True
        return response
    except (yt_dlp.utils.DownloadError, FileNotFoundError):
        app.logger.exception("Falha de extração/conversão")
        return "Não foi possível baixar esse vídeo. Ele pode estar indisponível, restrito ou bloqueado pelo YouTube.", 502
    except Exception:
        app.logger.exception("Falha inesperada durante download")
        return "Ocorreu um erro ao processar o arquivo. Tente novamente.", 500
    finally:
        if not handed_off:
            if directory is not None:
                shutil.rmtree(directory, ignore_errors=True)
            DOWNLOAD_LOCK.release()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")), debug=os.environ.get("FLASK_DEBUG") == "1")
