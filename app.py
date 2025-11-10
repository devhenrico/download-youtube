from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
from pathlib import Path

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

def limpar_arquivos_antigos():
    try:
        for arquivo in Path(DOWNLOAD_FOLDER).glob('*'):
            if arquivo.is_file():
                arquivo.unlink()
    except:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        formato = data.get('formato')
        
        if not url or not formato:
            return jsonify({'error': 'URL e formato são obrigatórios'}), 400
        
        if formato not in ['mp4', 'mp3']:
            return jsonify({'error': 'Formato inválido'}), 400
        
        if formato == 'mp4':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
            }
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if formato == 'mp3':
                filename = f"{info['title']}.mp3"
            else:
                filename = f"{info['title']}.mp4"
            
            filepath = Path(DOWNLOAD_FOLDER) / filename
        
        return jsonify({
            'success': True,
            'filename': filename,
            'title': info['title']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-file/<filename>')
def download_file(filename):
    try:
        filepath = Path(DOWNLOAD_FOLDER) / filename
        if filepath.exists():
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename
            )
        return jsonify({'error': 'Arquivo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    limpar_arquivos_antigos()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
