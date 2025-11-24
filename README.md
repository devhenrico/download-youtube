# 🎬 YouTube Downloader (MP3/MP4)

Um script em Python para baixar vídeos do YouTube em alta qualidade, nos formatos MP4 (vídeo) ou MP3 (áudio), utilizando a biblioteca [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## 🚀 Funcionalidades

- 📥 **Download de vídeos** do YouTube em MP4 (vídeo) ou MP3 (áudio)
- 🎧 **Extração automática de áudio** em MP3 usando ffmpeg
- 🏷️ **Nomeação automática** dos arquivos pelo título do vídeo
- 🖼️ **Download e inserção da miniatura** (thumbnail) nos arquivos MP3
- 🏷️ **Inserção de metadados** (nome do canal, título, etc.) nos arquivos baixados
- 🔄 **Interface interativa** via terminal
- ❌ **Validação de formatos** e URLs

## 🛠️ Requisitos

- Python 3.7 ou superior
- yt-dlp
- ffmpeg (para conversão de áudio)

## ⚙️ Instalação

1. Instale o Python: https://www.python.org/
2. Instale o yt-dlp:
	```bash
	pip install yt-dlp
	```
3. Instale o ffmpeg:
	- Windows: Baixe o executável em https://ffmpeg.org/download.html e adicione ao PATH
	- Linux: `sudo apt install ffmpeg`

## 💻 Como usar

1. Execute o script:
	```bash
	python download-youtube.py
	```
2. Digite a URL do vídeo do YouTube quando solicitado.
3. Escolha o formato desejado: `mp4` para vídeo ou `mp3` para áudio.
4. O arquivo será salvo na mesma pasta do script, com o nome do vídeo.
5. Os metadados (nome do canal, título, etc.) e a miniatura (para MP3) serão inseridos automaticamente.

## 📝 Licença

MIT License - sinta-se livre para usar em seus projetos!

## 👨‍💻 Autor

**Henrico**
- GitHub: [@devhenrico](https://github.com/devhenrico)