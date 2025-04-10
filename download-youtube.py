import yt_dlp

def baixar_video(url, formato):
    
    try:
        ydl_opts = {}
        if formato == 'mp4':
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'outtmpl': '%(title)s.%(ext)s',
            }

        elif formato == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
            }

        else:
            print("Formato inválido. Use 'mp4' ou 'mp3'.")
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("Download concluído!")   

    except Exception as e:
        print(f'Ocorreu um erro: {e}')

url = input("Digite a URL do vídeo: ")
formato = input("Digite o formato (mp4/mp3): ").strip().lower()

baixar_video(url, formato)
