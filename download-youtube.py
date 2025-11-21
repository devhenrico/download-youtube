import yt_dlp

def baixar_video(url, formato):
    
    try:
        if formato == 'mp4':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
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
            print("❌ Formato inválido. Use 'mp4' ou 'mp3'.")
            return False

        print(f"\n🔄 Iniciando download em formato {formato.upper()}...\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("\n✅ Download concluído com sucesso!")
            return True

    except Exception as e:
        print(f'\n❌ Ocorreu um erro: {e}')
        return False

def main():
    print("=" * 50)
    print("   YOUTUBE DOWNLOADER - MP3/MP4")
    print("=" * 50)
    
    while True:
        print("\n")
        url = input("Digite a URL do vídeo: ").strip()
        
        if not url:
            print("❌ URL não pode estar vazia!")
            continue
            
        formato = input("Digite o formato (mp4/mp3): ").strip().lower()
        
        if formato not in ['mp4', 'mp3']:
            print("❌ Formato inválido! Use 'mp4' ou 'mp3'.")
            continue
        
        baixar_video(url, formato)
        
        print("\n" + "=" * 50)
        continuar = input("\nDeseja baixar outro vídeo? (s/n): ").strip().lower()
        
        if continuar != 's':
            print("\n👋 Encerrando o programa...")
            break
    
    input("\nPressione ENTER para fechar...")

if __name__ == "__main__":
    main()
