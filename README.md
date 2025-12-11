# Convertidor de YouTube a MP4 (Premium GUI)

Aplicación de escritorio moderna para descargar videos de YouTube en máxima calidad, con historial de descargas e interfaz oscura amigable.

![Vista Principal](PLACEHOLDER_IMAGEN_PRINCIPAL)
*Interfaz principal de la aplicación.*

## Características

*   **Máxima Calidad**: Descarga videos en 1080p, 4K o la mejor calidad disponible fusionando video y audio automáticamente.
*   **Interfaz Moderna**: Diseño limpio y oscuro construido con `customtkinter`.
*   **Historial**: Registro persistente de tus descargas recientes.
*   **Acceso Rápido**: Botones para abrir la ubicación del archivo descargado fácilmente.

## Requisitos Previos

1.  **Python 3.8+**: [Descargar aquí](https://www.python.org/downloads/)
2.  **FFmpeg**: Esencial para procesar videos de alta resolución (1080p+).
    *   Asegúrate de tener `ffmpeg` en tus variables de entorno.
    *   Sin FFmpeg, la descarga se limitará a 720p.

## Instalación

1.  Abre una terminal en la carpeta del proyecto.
2.  Instala las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Inicia la aplicación ejecutando:

```bash
python gui_app.py
```

### Crear Acceso Directo

Para tener un icono en tu escritorio y abrir la app con un clic:

1.  Ejecuta el script de instalación:
    ```bash
    python crear_acceso_directo.py
    ```
2.  Busca el icono **YouTube Downloader** en tu escritorio.

1.  Pega el enlace de YouTube.
2.  Presiona **DESCARGAR**.
3.  ¡Listo! El video estará en `Videos/ConvertMp4`.

![Ejemplo de uso](PLACEHOLDER_OTRA_IMAGEN)

