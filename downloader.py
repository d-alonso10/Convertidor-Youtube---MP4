import yt_dlp
import sys
import os

def download_video(url):
    # Opciones para yt-dlp para obtener la mejor calidad posible en MP4
    ydl_opts = {
        # Selecciona el mejor video en mp4 y el mejor audio en m4a, y los une.
        # Si no encuentra eso, busca el mejor archivo mp4 disponible.
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo de salida
        'merge_output_format': 'mp4',    # Asegura que el contenedor final sea mp4
        'noplaylist': True,              # Descargar solo el video, no la playlist si es parte de una
    }

    print(f"Iniciando proceso para: {url}")
    print("Nota: Para la máxima calidad (1080p+), asegúrate de tener FFmpeg instalado en tu sistema.")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            print(f"\n¡Descarga completada exitosamente!")
            print(f"Video guardado como: {video_title}.mp4")
    except Exception as e:
        print(f"\nOcurrió un error durante la descarga: {e}")

if __name__ == "__main__":
    print("--- Descargador de YouTube a MP4 (Máxima Calidad) ---")
    
    # Permitir pasar la URL como argumento o pedirla
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Por favor, ingresa el link del video de YouTube: ").strip()
    
    if url:
        download_video(url)
    else:
        print("Error: No se ingresó ninguna URL.")
