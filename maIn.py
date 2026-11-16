import customtkinter as ctk
from PIL import Image

# Pengaturan Tema CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class EduDocApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi Window Utama
        self.title("EduDoc Desktop Utility")
        self.geometry("900 x 600")
        self.minsize(800, 500)

        # Konfigurasi Grid Layout (1 Kolom Sidebar, 1 Kolom Konten Utama)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------- SIDEBAR -------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Logo / Judul Aplikasi
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="EduDoc\nUtility", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Tombol Navigasi Sidebar
        self.btn_image = ctk.CTkButton(
            self.sidebar_frame, text="Image Utility", command=self.show_image_tab
        )
        self.btn_image.grid(row=1, column=0, padx=20, pady=10)

        self.btn_pdf = ctk.CTkButton(
            self.sidebar_frame, text="PDF Utility", command=self.show_pdf_tab
        )
        self.btn_pdf.grid(row=2, column=0, padx=20, pady=10)

        self.btn_about = ctk.CTkButton(
            self.sidebar_frame, text="About", command=self.show_about_tab
        )
        self.btn_about.grid(row=3, column=0, padx=20, pady=10)

        # Indikator Status
        self.status_label = ctk.CTkLabel(
            self.sidebar_frame, text="Status: Ready", font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=5, column=0, padx=20, pady=20)

        # ------------------- KONTEN UTAMA -------------------
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.content_label = ctk.CTkLabel(
            self.main_frame, 
            text="Selamat Datang di EduDoc Desktop Utility", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.content_label.pack(expand=True)

    # Fungsi Perpindahan Tab (Sementara)
    def show_image_tab(self):
        self.content_label.configure(text="Tab Image Utility (Dalam Pengembangan)")

    def show_pdf_tab(self):
        self.content_label.configure(text="Tab PDF Utility (Dalam Pengembangan)")

    def show_about_tab(self):
        self.content_label.configure(text="EduDoc Desktop Utility v1.0\nDibuat untuk Tugas Sekolah")

if __name__ == "__main__":
    app = EduDocApp()
    app.mainloop()