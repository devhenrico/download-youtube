from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
from downloader import download_media, is_youtube_url

def baixar_video(url: str, formato: str) -> bool:
    formato = formato.strip().lower()
    if formato not in {"mp3", "mp4"} or not is_youtube_url(url):
        print("Informe um link válido do YouTube e MP3 ou MP4.")
        return False

    try:
        with TemporaryDirectory(prefix="youtube-cli-") as temporary_directory:
            print(f"\nPreparando {formato.upper()} na melhor qualidade disponível...")
            src, filename = download_media(url, formato, temporary_directory)
            target = Path.cwd() / filename
            suffix = 2
            while target.exists():
                target = Path.cwd() / f"{Path(filename).stem} ({suffix}){Path(filename).suffix}"
                suffix += 1
            shutil.move(str(src), str(target))
        print(f"\nDownload concluído: {target}")
        return True
    except Exception as error:
        print(f"\nNão foi possível concluir o download: {error}")
        return False

def main():
    print("=" * 48)
    print("     DOWNLOAD YOUTUBE - MP4 / MP3")
    print("=" * 48)
    while True:
        print()
        url = input("Cole a URL do vídeo: ").strip()
        formato = input("Formato (mp4/mp3): ").strip()
        baixar_video(url, formato)
        if input("\nBaixar outro? (s/n): ").strip().lower() != "s":
            break

if __name__ == "__main__":
    main()
