import customtkinter as ctk
import yt_dlp
import threading
import os
import json
import subprocess
from datetime import datetime

# Configuración inicial de la apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

HISTORY_FILE = "history.json"

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Convertidor YouTube a MP4 - Premium")
        self.geometry("750x550")
        self.resizable(False, False)

        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="YouTube Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(side="left")

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Máxima Calidad MP4", font=ctk.CTkFont(size=14), text_color="gray")
        self.subtitle_label.pack(side="left", padx=10, pady=(8, 0))

        # --- Input Area ---
        self.input_frame = ctk.CTkFrame(self, corner_radius=15)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Pega el link del video aquí...", height=40, font=ctk.CTkFont(size=14))
        self.url_entry.grid(row=0, column=0, padx=15, pady=15, sticky="ew")

        self.download_button = ctk.CTkButton(self.input_frame, text="DESCARGAR", height=40, font=ctk.CTkFont(size=14, weight="bold"), command=self.start_download_thread)
        self.download_button.grid(row=0, column=1, padx=(0, 15), pady=15)

        self.status_label = ctk.CTkLabel(self.input_frame, text="Listo para descargar", text_color="gray")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # --- History Dashboard ---
        self.history_label = ctk.CTkLabel(self, text="Historial de Conversiones", font=ctk.CTkFont(size=16, weight="bold"))
        self.history_label.grid(row=2, column=0, sticky="w", padx=25, pady=(10, 5))

        self.history_frame = ctk.CTkScrollableFrame(self, corner_radius=15, label_text="Videos Descargados")
        self.history_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.history_frame.grid_columnconfigure(0, weight=1)

        # Cargar historial
        self.history_data = self.load_history()
        self.refresh_history_ui()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self, video_info):
        self.history_data.insert(0, video_info) # Agregar al principio
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, indent=4, ensure_ascii=False)
        self.refresh_history_ui()

    def refresh_history_ui(self):
        # Limpiar frame
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not self.history_data:
            empty_label = ctk.CTkLabel(self.history_frame, text="No hay descargas recientes", text_color="gray")
            empty_label.pack(pady=20)
            return

        for item in self.history_data:
            self.create_history_item(item)

    def create_history_item(self, item):
        card = ctk.CTkFrame(self.history_frame, corner_radius=10, fg_color=("gray85", "gray20"))
        card.pack(fill="x", pady=5, padx=5)
        
        # Icono o estado
        status_lbl = ctk.CTkLabel(card, text="🎬", font=ctk.CTkFont(size=20))
        status_lbl.pack(side="left", padx=(10, 0))

        # Info container
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        title_lbl = ctk.CTkLabel(info_frame, text=item.get("title", "Desconocido"), font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        title_lbl.pack(fill="x")

        date_lbl = ctk.CTkLabel(info_frame, text=item.get("date", ""), font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        date_lbl.pack(fill="x")

        # Botón Abrir Carpeta
        open_btn = ctk.CTkButton(card, text="📂 Abrir", width=80, height=30, 
                                 fg_color="#3B8ED0", hover_color="#36719F",
                                 command=lambda p=item.get("file_path"): self.open_file_location(p))
        open_btn.pack(side="right", padx=10, pady=10)

    def open_file_location(self, file_path):
        if not file_path or not os.path.exists(file_path):
            # Si no existe el archivo específico, intentamos abrir la carpeta actual
            file_path = os.getcwd()
        
        try:
            # Comando para Windows que selecciona el archivo en el explorador
            subprocess.Popen(f'explorer /select,"{os.path.normpath(file_path)}"')
        except Exception as e:
            print(f"Error al abrir carpeta: {e}")
            # Fallback simple
            try:
                os.startfile(os.path.dirname(file_path) if os.path.isfile(file_path) else file_path)
            except:
                pass

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="❌ Por favor ingresa una URL válida", text_color="#FF5555")
            return

        self.download_button.configure(state="disabled", text="Descargando...")
        self.status_label.configure(text="⏳ Iniciando descarga... (Esto puede tardar unos segundos)", text_color="#3B8ED0")
        
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.start()

    def download_video(self, url):
        # Definir carpeta de destino: Videos/ConvertMp4
        videos_dir = os.path.join(os.environ['USERPROFILE'], 'Videos')
        save_dir = os.path.join(videos_dir, 'ConvertMp4')
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.update_status("🔍 Obteniendo información del video...")
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', 'Video sin título')
                
                # Intentar obtener la ruta del archivo final
                filename = ydl.prepare_filename(info_dict)
                # Asegurar extensión mp4 si se hizo merge
                base, _ = os.path.splitext(filename)
                final_filename = base + ".mp4"
                abs_path = os.path.abspath(final_filename)

                # Guardar en historial
                new_entry = {
                    "title": video_title,
                    "url": url,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "file_path": abs_path
                }
                
                # Actualizar UI en el hilo principal
                self.after(0, lambda: self.finish_download(new_entry))
                
        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def update_status(self, message):
        self.after(0, lambda: self.status_label.configure(text=message, text_color="#3B8ED0"))

    def finish_download(self, entry):
        self.save_history(entry)
        self.url_entry.delete(0, "end")
        self.status_label.configure(text=f"✅ ¡Descarga completada! - {entry['title']}", text_color="#2CC985")
        self.download_button.configure(state="normal", text="DESCARGAR")

    def show_error(self, error_msg):
        self.status_label.configure(text="❌ Error al descargar. Verifica el link o tu conexión.", text_color="#FF5555")
        self.download_button.configure(state="normal", text="DESCARGAR")

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
