# 🎬 YouTube Downloader

> Uma aplicação web minimalista para baixar vídeos e áudios do YouTube em alta qualidade.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Características

- 🎵 **Download de áudio** (MP3 melhor qualidade)
- 🎥 **Download de vídeo** (MP4 melhor qualidade)
- 🎨 **Design minimalista** (preto, branco e vermelho)
- 📱 **Responsivo** - funciona em desktop e mobile
- ⚡ **Rápido e simples** - interface intuitiva
- 🔒 **Sem banco de dados** - downloads diretos

## 🛠️ Tecnologias

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask + yt-dlp
- **FFmpeg**: Conversão de áudio/vídeo
- **Deploy**: Render.com + Gunicorn

## 📦 Instalação Local

### Pré-requisitos

- Python 3.11+
- FFmpeg instalado no sistema (adicionado ao PATH)

## 📁 Estrutura do Projeto

```
download-youtube/
├── app.py                 # Aplicação Flask
├── requirements.txt       # Dependências Python
├── render.yaml           # Configuração Render
├── templates/
│   └── index.html        # Interface web
├── static/
│   ├── style.css         # Estilos (preto/branco/vermelho)
│   └── script.js         # Lógica do cliente
├── downloads/            # Arquivos temporários
└── README.md
```

## 🎯 Uso

1. Cole a URL do vídeo do YouTube
2. Escolha o formato (MP4 ou MP3)
3. Clique em "Baixar Agora"
4. Aguarde o processamento
5. Download automático!

## 📝 Licença

MIT License - sinta-se livre para usar em seus projetos!

## 👨‍💻 Autor

**Henrico**
- GitHub: [@devhenrico](https://github.com/devhenrico)