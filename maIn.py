import warnings
warnings.filterwarnings("ignore")

import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

# Import modul backend
from core.image_module import process_image
from core.pdf_module import merge_pdfs, split_pdf, pdf_to_docx

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class EduDocApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EduDoc Desktop Utility")
        self.geometry("950x700")
        self.minsize(850, 600)
        self.configure(fg_color="#f3f4f6")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------- SIDEBAR (PUTIH BERSIH) -------------------
        self.sidebar_frame = ctk.CTkFrame(
            self, width=200, corner_radius=0, fg_color="#ffffff", border_width=1, border_color="#e5e7eb"
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="EduDoc\nUtility", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#111827"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 30))

        self.btn_image = ctk.CTkButton(
            self.sidebar_frame, 
            text="Image Utility", 
            fg_color="#e5e7eb", 
            text_color="#111827", 
            hover_color="#d1d5db",
            command=self.show_image_tab
        )
        self.btn_image.grid(row=1, column=0, padx=20, pady=8)

        self.btn_pdf = ctk.CTkButton(
            self.sidebar_frame, 
            text="PDF Utility", 
            fg_color="#e5e7eb", 
            text_color="#111827", 
            hover_color="#d1d5db",
            command=self.show_pdf_tab
        )
        self.btn_pdf.grid(row=2, column=0, padx=20, pady=8)

        self.btn_about = ctk.CTkButton(
            self.sidebar_frame, 
            text="About", 
            fg_color="#e5e7eb", 
            text_color="#111827", 
            hover_color="#d1d5db",
            command=self.show_about_tab
        )
        self.btn_about.grid(row=3, column=0, padx=20, pady=8)

        self.status_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Status: Ready", 
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        )
        self.status_label.grid(row=5, column=0, padx=20, pady=20)

        # ------------------- KONTEN UTAMA (PUTIH) -------------------
        self.main_frame = ctk.CTkFrame(
            self, corner_radius=12, fg_color="#ffffff", border_width=1, border_color="#e5e7eb"
        )
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Variable Simpan State
        self.selected_image_path = ""
        self.selected_image_info = ""
        self.pdf_merge_list = []
        self.selected_split_pdf = ""
        self.selected_docx_pdf = ""

        # Tampilkan Tab Image secara default
        self.show_image_tab()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def notify_and_open_folder(self, message, file_path):
        open_dir = messagebox.askyesno(
            "Sukses", 
            f"{message}\n\nApakah Anda ingin langsung membuka folder penyimpanan?"
        )
        if open_dir:
            folder_path = os.path.dirname(os.path.abspath(file_path))
            os.startfile(folder_path)

    def highlight_nav(self, active_btn):
        for btn in [self.btn_image, self.btn_pdf, self.btn_about]:
            if btn == active_btn:
                btn.configure(fg_color="#374151", text_color="#ffffff", hover_color="#1f2937")
            else:
                btn.configure(fg_color="#e5e7eb", text_color="#111827", hover_color="#d1d5db")

    # ================= 1. TAB IMAGE UTILITY =================
    def show_image_tab(self):
        self.highlight_nav(self.btn_image)
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame, text="Image Utility", font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827"
        )
        title.pack(anchor="w", padx=25, pady=(25, 10))

        # File Selector
        file_frame = ctk.CTkFrame(self.main_frame, fg_color="#f9fafb", border_width=1, border_color="#e5e7eb")
        file_frame.pack(fill="x", padx=25, pady=10)

        self.btn_select_img = ctk.CTkButton(
            file_frame, text="Pilih Gambar", fg_color="#4b5563", hover_color="#374151", command=self.select_image_file
        )
        self.btn_select_img.pack(side="left", padx=12, pady=12)

        display_text = os.path.basename(self.selected_image_path) if self.selected_image_path else "Belum ada gambar terpilih"
        text_color = "#111827" if self.selected_image_path else "#6b7280"
        self.lbl_file_path = ctk.CTkLabel(file_frame, text=display_text, text_color=text_color)
        self.lbl_file_path.pack(side="left", padx=10, pady=12)

        self.lbl_img_info = ctk.CTkLabel(
            file_frame, text=self.selected_image_info, text_color="#6b7280", font=ctk.CTkFont(size=12)
        )
        self.lbl_img_info.pack(side="right", padx=15, pady=12)

        # Options Section
        opt_frame = ctk.CTkFrame(self.main_frame, fg_color="#f9fafb", border_width=1, border_color="#e5e7eb")
        opt_frame.pack(fill="x", padx=25, pady=10)

        lbl_format = ctk.CTkLabel(opt_frame, text="Target Format:", text_color="#111827")
        lbl_format.grid(row=0, column=0, padx=12, pady=12, sticky="w")
        
        self.combo_format = ctk.CTkComboBox(
            opt_frame, values=["JPEG", "PNG"], fg_color="#ffffff", border_color="#d1d5db", text_color="#111827"
        )
        self.combo_format.set("JPEG")
        self.combo_format.grid(row=0, column=1, padx=12, pady=12)

        lbl_quality = ctk.CTkLabel(opt_frame, text="Kualitas (Quality):", text_color="#111827")
        lbl_quality.grid(row=1, column=0, padx=12, pady=12, sticky="w")

        self.slider_quality = ctk.CTkSlider(
            opt_frame, from_=10, to=100, number_of_steps=90, button_color="#374151", progress_color="#6b7280", command=self.update_quality_label
        )
        self.slider_quality.set(85)
        self.slider_quality.grid(row=1, column=1, padx=12, pady=12)

        self.lbl_quality_val = ctk.CTkLabel(opt_frame, text="85%", text_color="#111827", font=ctk.CTkFont(weight="bold"))
        self.lbl_quality_val.grid(row=1, column=2, padx=12, pady=12)

        # Resize Section
        resize_frame = ctk.CTkFrame(self.main_frame, fg_color="#f9fafb", border_width=1, border_color="#e5e7eb")
        resize_frame.pack(fill="x", padx=25, pady=10)

        self.chk_resize = ctk.CTkCheckBox(
            resize_frame, text="Aktifkan Resize (Opsional)", text_color="#111827", fg_color="#374151", hover_color="#1f2937"
        )
        self.chk_resize.grid(row=0, column=0, columnspan=2, padx=12, pady=12, sticky="w")

        lbl_w = ctk.CTkLabel(resize_frame, text="Width (px):", text_color="#111827")
        lbl_w.grid(row=1, column=0, padx=12, pady=6, sticky="w")
        self.entry_width = ctk.CTkEntry(
            resize_frame, placeholder_text="800", fg_color="#ffffff", border_color="#d1d5db", text_color="#111827"
        )
        self.entry_width.grid(row=1, column=1, padx=12, pady=6)

        lbl_h = ctk.CTkLabel(resize_frame, text="Height (px):", text_color="#111827")
        lbl_h.grid(row=2, column=0, padx=12, pady=(6, 12), sticky="w")
        self.entry_height = ctk.CTkEntry(
            resize_frame, placeholder_text="600", fg_color="#ffffff", border_color="#d1d5db", text_color="#111827"
        )
        self.entry_height.grid(row=2, column=1, padx=12, pady=(6, 12))

        # Process Button
        self.btn_process_img = ctk.CTkButton(
            self.main_frame, 
            text="PROSES GAMBAR", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#374151",
            hover_color="#1f2937",
            text_color="#ffffff",
            height=40,
            command=self.handle_process_image
        )
        self.btn_process_img.pack(fill="x", padx=25, pady=20)

    def select_image_file(self):
        file_path = filedialog.askopenfilename(
            title="Pilih File Gambar",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.lbl_file_path.configure(
                text=os.path.basename(file_path), text_color="#111827"
            )

            size_bytes = os.path.getsize(file_path)
            size_str = f"{size_bytes / (1024 * 1024):.2f} MB" if size_bytes >= 1024 * 1024 else f"{size_bytes / 1024:.1f} KB"

            with Image.open(file_path) as img:
                w, h = img.size

            self.selected_image_info = f"Resolusi: {w}x{h} px  |  Ukuran: {size_str}"
            self.lbl_img_info.configure(text=self.selected_image_info)

    def update_quality_label(self, value):
        self.lbl_quality_val.configure(text=f"{int(value)}%")

    def handle_process_image(self):
        if not self.selected_image_path:
            messagebox.showwarning("Peringatan", "Pilih file gambar terlebih dahulu!")
            return

        fmt = self.combo_format.get().lower()
        ext = ".jpg" if fmt == "jpeg" else ".png"
        ftype = [("JPEG File", "*.jpg")] if fmt == "jpeg" else [("PNG File", "*.png")]

        save_path = filedialog.asksaveasfilename(defaultextension=ext, filetypes=ftype)
        if not save_path:
            return

        resize_dim = None
        if self.chk_resize.get() == 1:
            try:
                w = int(self.entry_width.get())
                h = int(self.entry_height.get())
                resize_dim = (w, h)
            except ValueError:
                messagebox.showerror("Error", "Nilai Width dan Height harus berupa angka valid!")
                return

        try:
            process_image(
                input_path=self.selected_image_path,
                output_path=save_path,
                target_format=self.combo_format.get(),
                quality=int(self.slider_quality.get()),
                resize_dim=resize_dim
            )
            self.status_label.configure(text="Status: Image Saved!")
            # LANGKAH 2: Pemanggilan fungsi buka folder
            self.notify_and_open_folder("Gambar berhasil diproses dan disimpan!", save_path)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memproses gambar:\n{str(e)}")

    # ================= 2. TAB PDF UTILITY =================
    def show_pdf_tab(self):
        self.highlight_nav(self.btn_pdf)
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame, text="PDF Utility", font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827"
        )
        title.pack(anchor="w", padx=25, pady=(25, 10))

        # Menu Pilihan Sub-Fitur PDF
        self.pdf_mode_var = ctk.StringVar(value="Merge PDF")
        seg_btn = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["Merge PDF", "Split PDF", "PDF to Word"],
            variable=self.pdf_mode_var,
            fg_color="#e5e7eb",
            selected_color="#374151",
            selected_hover_color="#1f2937",
            unselected_color="#e5e7eb",
            unselected_hover_color="#d1d5db",
            text_color="#111827",
            command=self.switch_pdf_subview
        )
        seg_btn.pack(fill="x", padx=25, pady=10)

        # Kontainer khusus untuk isi sub-fitur PDF
        self.pdf_sub_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#f9fafb", border_width=1, border_color="#e5e7eb"
        )
        self.pdf_sub_frame.pack(fill="both", expand=True, padx=25, pady=(10, 25))

        self.switch_pdf_subview("Merge PDF")

    def switch_pdf_subview(self, mode):
        for widget in self.pdf_sub_frame.winfo_children():
            widget.destroy()

        if mode == "Merge PDF":
            btn_add_pdfs = ctk.CTkButton(
                self.pdf_sub_frame, text="Pilih / Tambah File PDF", fg_color="#4b5563", hover_color="#374151", command=self.add_merge_pdfs
            )
            btn_add_pdfs.pack(padx=20, pady=(20, 10), anchor="w")

            self.lbl_merge_count = ctk.CTkLabel(
                self.pdf_sub_frame, text=f"{len(self.pdf_merge_list)} File PDF terpilih", font=ctk.CTkFont(size=14), text_color="#111827"
            )
            self.lbl_merge_count.pack(padx=20, pady=5, anchor="w")

            btn_run_merge = ctk.CTkButton(
                self.pdf_sub_frame, text="GABUNGKAN PDF", font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#374151", hover_color="#1f2937", height=40, command=self.handle_merge_pdfs
            )
            btn_run_merge.pack(fill="x", padx=20, pady=30)

        elif mode == "Split PDF":
            btn_select_split = ctk.CTkButton(
                self.pdf_sub_frame, text="Pilih File PDF", fg_color="#4b5563", hover_color="#374151", command=self.select_split_pdf
            )
            btn_select_split.pack(padx=20, pady=(20, 10), anchor="w")

            split_txt = os.path.basename(self.selected_split_pdf) if self.selected_split_pdf else "Belum ada file terpilih"
            split_clr = "#111827" if self.selected_split_pdf else "#6b7280"
            self.lbl_split_file = ctk.CTkLabel(self.pdf_sub_frame, text=split_txt, text_color=split_clr, font=ctk.CTkFont(size=13))
            self.lbl_split_file.pack(padx=20, pady=2, anchor="w")

            split_opts = ctk.CTkFrame(self.pdf_sub_frame, fg_color="#ffffff", border_width=1, border_color="#e5e7eb")
            split_opts.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(split_opts, text="Dari Halaman:", text_color="#111827").grid(row=0, column=0, padx=12, pady=10, sticky="w")
            self.entry_start_p = ctk.CTkEntry(
                split_opts, placeholder_text="1", fg_color="#f9fafb", border_color="#d1d5db", text_color="#111827"
            )
            self.entry_start_p.grid(row=0, column=1, padx=12, pady=10)

            ctk.CTkLabel(split_opts, text="Sampai Halaman:", text_color="#111827").grid(row=1, column=0, padx=12, pady=10, sticky="w")
            self.entry_end_p = ctk.CTkEntry(
                split_opts, placeholder_text="2", fg_color="#f9fafb", border_color="#d1d5db", text_color="#111827"
            )
            self.entry_end_p.grid(row=1, column=1, padx=12, pady=10)

            btn_run_split = ctk.CTkButton(
                self.pdf_sub_frame, text="PISAHKAN PDF", font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#374151", hover_color="#1f2937", height=40, command=self.handle_split_pdf
            )
            btn_run_split.pack(fill="x", padx=20, pady=20)

        elif mode == "PDF to Word":
            btn_select_docx = ctk.CTkButton(
                self.pdf_sub_frame, text="Pilih File PDF", fg_color="#4b5563", hover_color="#374151", command=self.select_docx_pdf
            )
            btn_select_docx.pack(padx=20, pady=(20, 10), anchor="w")

            docx_txt = os.path.basename(self.selected_docx_pdf) if self.selected_docx_pdf else "Belum ada file terpilih"
            docx_clr = "#111827" if self.selected_docx_pdf else "#6b7280"
            self.lbl_docx_file = ctk.CTkLabel(self.pdf_sub_frame, text=docx_txt, text_color=docx_clr, font=ctk.CTkFont(size=13))
            self.lbl_docx_file.pack(padx=20, pady=2, anchor="w")

            btn_run_docx = ctk.CTkButton(
                self.pdf_sub_frame, text="KONVERSI KE DOCX", font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#374151", hover_color="#1f2937", height=40, command=self.handle_pdf_to_docx
            )
            btn_run_docx.pack(fill="x", padx=20, pady=30)

    # Handlers PDF
    def add_merge_pdfs(self):
        files = filedialog.askopenfilenames(title="Pilih File PDF", filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.pdf_merge_list.extend(files)
            self.lbl_merge_count.configure(text=f"{len(self.pdf_merge_list)} File PDF terpilih")

    def handle_merge_pdfs(self):
        if len(self.pdf_merge_list) < 2:
            messagebox.showwarning("Peringatan", "Pilih minimal 2 file PDF untuk digabungkan!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if save_path:
            try:
                merge_pdfs(self.pdf_merge_list, save_path)
                self.pdf_merge_list.clear()
                self.lbl_merge_count.configure(text="0 File PDF terpilih")
                self.status_label.configure(text="Status: PDFs Merged!")
                # LANGKAH 2: Pemanggilan fungsi buka folder
                self.notify_and_open_folder("File PDF berhasil digabungkan!", save_path)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menggabungkan PDF:\n{str(e)}")

    def select_split_pdf(self):
        file_path = filedialog.askopenfilename(title="Pilih File PDF", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.selected_split_pdf = file_path
            self.lbl_split_file.configure(text=os.path.basename(file_path), text_color="#111827")

    def handle_split_pdf(self):
        if not self.selected_split_pdf:
            messagebox.showwarning("Peringatan", "Pilih file PDF terlebih dahulu!")
            return
        try:
            start = int(self.entry_start_p.get())
            end = int(self.entry_end_p.get())
            if start < 1 or end < start:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rentang halaman tidak valid!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if save_path:
            try:
                split_pdf(self.selected_split_pdf, save_path, start, end)
                self.status_label.configure(text="Status: PDF Split!")
                # LANGKAH 2: Pemanggilan fungsi buka folder
                self.notify_and_open_folder("Halaman PDF berhasil dipisahkan!", save_path)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memisahkan PDF:\n{str(e)}")

    def select_docx_pdf(self):
        file_path = filedialog.askopenfilename(title="Pilih File PDF", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.selected_docx_pdf = file_path
            self.lbl_docx_file.configure(text=os.path.basename(file_path), text_color="#111827")

    def handle_pdf_to_docx(self):
        if not self.selected_docx_pdf:
            messagebox.showwarning("Peringatan", "Pilih file PDF terlebih dahulu!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
        if save_path:
            try:
                pdf_to_docx(self.selected_docx_pdf, save_path)
                self.status_label.configure(text="Status: Converted to DOCX!")
                # LANGKAH 2: Pemanggilan fungsi buka folder
                self.notify_and_open_folder("File PDF berhasil dikonversi ke format Word (.docx)!", save_path)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengonversi PDF:\n{str(e)}")

    # ================= 3. TAB ABOUT =================
    def show_about_tab(self):
        self.highlight_nav(self.btn_about)
        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame, text="About EduDoc Utility", font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827"
        )
        title.pack(anchor="w", padx=25, pady=(25, 10))

        info_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#f9fafb", border_width=1, border_color="#e5e7eb"
        )
        info_frame.pack(fill="both", expand=True, padx=25, pady=(10, 25))

        app_title = ctk.CTkLabel(
            info_frame, 
            text="EduDoc Desktop Utility v1.0", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#111827"
        )
        app_title.pack(anchor="w", padx=20, pady=(20, 10))

        app_desc = (
            "Aplikasi desktop multifungsi berbasis Python untuk membantu kebutuhan pemrosesan "
            "dokumen harian, seperti optimasi/resize gambar, penggabungan & pemisahan halaman PDF, "
            "serta konversi dokumen PDF menjadi dokumen Word yang dapat diedit."
        )
        lbl_desc = ctk.CTkLabel(
            info_frame, text=app_desc, justify="left", wraplength=600, font=ctk.CTkFont(size=13), text_color="#374151"
        )
        lbl_desc.pack(anchor="w", padx=20, pady=(0, 15))

        tech_title = ctk.CTkLabel(
            info_frame, text="Teknologi yang Digunakan:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#111827"
        )
        tech_title.pack(anchor="w", padx=20, pady=(5, 5))

        tech_stack = (
            "• Language: Python 3\n"
            "• GUI Framework: CustomTkinter\n"
            "• Image Processing: Pillow (PIL)\n"
            "• PDF Engine: PyPDF & pdf2docx"
        )
        lbl_tech = ctk.CTkLabel(
            info_frame, text=tech_stack, justify="left", font=ctk.CTkFont(size=13), text_color="#374151"
        )
        lbl_tech.pack(anchor="w", padx=25, pady=(0, 20))

if __name__ == "__main__":
    app = EduDocApp()
    app.mainloop()