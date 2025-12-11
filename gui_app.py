import customtkinter as ctk
import yt_dlp
import threading
import os
import json
import subprocess
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

HISTORY_FILE = "history.json"

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Convertidor YouTube a MP4 - Premium")
        self.geometry("800x630")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 20))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="YouTube Downloader", font=ctk.CTkFont(family="Roboto", size=28, weight="bold"))
        self.title_label.pack(side="left")

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Premium Edition", font=ctk.CTkFont(family="Roboto", size=14), text_color="#3D5AFE")
        self.subtitle_label.pack(side="left", padx=10, pady=(12, 0))

        self.input_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#2b2b2b")
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Pegar enlace de YouTube aquí...", height=50, border_width=0, fg_color="#1f1f1f", font=ctk.CTkFont(size=14))
        self.url_entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Color solicitado #170078
        self.download_button = ctk.CTkButton(self.input_frame, text="DESCARGAR MP4", height=50, fg_color="#170078", hover_color="#304ffe", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), corner_radius=15, command=self.start_download_thread)
        self.download_button.grid(row=0, column=1, padx=(0, 20), pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.input_frame, height=10, corner_radius=5, progress_color="#3D5AFE", fg_color="#111111")
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(self.input_frame, text="Listo para iniciar", text_color="gray70", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(0, 15))

        self.history_label = ctk.CTkLabel(self, text="Descargas Recientes", font=ctk.CTkFont(size=18, weight="bold"))
        self.history_label.grid(row=3, column=0, sticky="w", padx=35, pady=(20, 10))

        self.history_frame = ctk.CTkScrollableFrame(self, corner_radius=20, fg_color="#2b2b2b", label_text="")
        self.history_frame.grid(row=4, column=0, sticky="nsew", padx=30, pady=(0, 30))
        self.history_frame.grid_columnconfigure(0, weight=1)

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
        self.history_data.insert(0, video_info)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, indent=4, ensure_ascii=False)
        self.refresh_history_ui()

    def refresh_history_ui(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not self.history_data:
            empty_label = ctk.CTkLabel(self.history_frame, text="Tu historial aparecerá aquí", text_color="gray50", font=ctk.CTkFont(size=14))
            empty_label.pack(pady=40)
            return

        for item in self.history_data:
            self.create_history_item(item)

    def create_history_item(self, item):
        card = ctk.CTkFrame(self.history_frame, corner_radius=15, fg_color="#333333")
        card.pack(fill="x", pady=6, padx=5)
        
        icon_lbl = ctk.CTkLabel(card, text="▶", font=ctk.CTkFont(size=18), text_color="#3D5AFE")
        icon_lbl.pack(side="left", padx=15)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=10)

        title_lbl = ctk.CTkLabel(info_frame, text=item.get("title", "Desconocido"), font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        title_lbl.pack(fill="x")

        date_lbl = ctk.CTkLabel(info_frame, text=item.get("date", ""), font=ctk.CTkFont(size=11), text_color="gray70", anchor="w")
        date_lbl.pack(fill="x")

        open_btn = ctk.CTkButton(card, text="Abrir", width=70, height=32, corner_radius=10,
                                 fg_color="#1a1a1a", hover_color="#333333",
                                 font=ctk.CTkFont(size=12),
                                 command=lambda p=item.get("file_path"): self.open_file_location(p))
        open_btn.pack(side="right", padx=15, pady=10)

    def open_file_location(self, file_path):
        if not file_path or not os.path.exists(file_path):
            file_path = os.getcwd()
        try:
            subprocess.Popen(f'explorer /select,"{os.path.normpath(file_path)}"')
        except Exception as e:
            try:
                os.startfile(os.path.dirname(file_path) if os.path.isfile(file_path) else file_path)
            except:
                pass

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="❌ Enlace requerido", text_color="#FF5555")
            return

        self.download_button.configure(state="disabled", text="INICIANDO...", fg_color="#100055")
        self.status_label.configure(text="⏳ Conectando con YouTube...", text_color="#3D5AFE")
        
        # Animación de entrada de la barra de progreso
        self.progress_bar.grid(row=1, column=0, columnspan=2, headers=20, pady=(0, 15), sticky="ew", padx=20)
        self.progress_bar.set(0)
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(0, 15)) # Mover label abajo

        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%', '')
                progress = float(p) / 100
                self.after(0, lambda: self.progress_bar.set(progress))
                self.after(0, lambda: self.status_label.configure(text=f"⬇️ Descargando: {d.get('_percent_str')}"))
            except:
                pass
        elif d['status'] == 'finished':
            self.after(0, lambda: self.progress_bar.set(1))
            self.after(0, lambda: self.status_label.configure(text="✨ Procesando video final..."))

    def download_video(self, url):
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
            'progress_hooks': [self.progress_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', 'Video sin título')
                filename = ydl.prepare_filename(info_dict)
                base, _ = os.path.splitext(filename)
                final_filename = base + ".mp4"
                abs_path = os.path.abspath(final_filename)

                new_entry = {
                    "title": video_title,
                    "url": url,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "file_path": abs_path
                }
                self.after(0, lambda: self.finish_download(new_entry))
                
        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def update_status(self, message):
        self.after(0, lambda: self.status_label.configure(text=message, text_color="#3D5AFE"))

    def finish_download(self, entry):
        self.save_history(entry)
        self.url_entry.delete(0, "end")
        self.status_label.configure(text=f"✅ Completado: {entry['title']}", text_color="#00E676")
        self.download_button.configure(state="normal", text="DESCARGAR MP4", fg_color="#170078")
        self.progress_bar.grid_forget() # Ocultar barra al finalizar
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 15)) # Restaurar posición label

    def show_error(self, error_msg):
        self.status_label.configure(text="❌ Error en la descarga", text_color="#FF5555")
        self.download_button.configure(state="normal", text="DESCARGAR MP4", fg_color="#170078")
        self.progress_bar.grid_forget()

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
