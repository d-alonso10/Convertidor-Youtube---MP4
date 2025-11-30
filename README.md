# Convertidor de YouTube a MP4 (Máxima Calidad)

Este sistema utiliza Python y la librería `yt-dlp` para descargar videos de YouTube en la mejor calidad posible.

## Requisitos Previos

1.  **Python**: Debes tener Python instalado.
2.  **FFmpeg** (Importante para Alta Calidad):
    *   YouTube separa el video y el audio para calidades altas (1080p, 4K, etc.).
    *   Para unir estos archivos y obtener un solo MP4 de alta calidad, **necesitas tener FFmpeg instalado** y agregado a las variables de entorno de tu sistema (PATH).
    *   Si no tienes FFmpeg, el script descargará la mejor calidad "única" disponible (generalmente 720p).

## Instalación

1.  Abre una terminal en esta carpeta.
2.  Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Ejecuta el script desde la terminal:

```bash
python downloader.py
```

Luego pega el enlace del video cuando se te solicite.

O pásalo directamente como argumento:

```bash
python downloader.py "https://www.youtube.com/watch?v=..."
```
