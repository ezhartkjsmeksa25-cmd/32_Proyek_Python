from pypdf import PdfMerger, PdfReader, PdfWriter
from pdf2docx import Converter

def merge_pdfs(pdf_list, output_path):
    """Menggabungkan beberapa file PDF menjadi satu file."""
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def split_pdf(input_pdf, output_pdf, start_page, end_page):
    """
    Memisah halaman PDF dari start_page hingga end_page.
    Catatan: Halaman dimulai dari angka 1 untuk kenyamanan user.
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Konversi indeks halaman (1-based ke 0-based)
    for i in range(start_page - 1, end_page):
        if i < len(reader.pages):
            writer.add_page(reader.pages[i])
            
    with open(output_pdf, "wb") as f:
        writer.write(f)

def pdf_to_docx(input_pdf, output_docx):
    """Mengonversi file PDF menjadi dokumen Word (.docx)."""
    cv = Converter(input_pdf)
    cv.convert(output_docx, start=0, end=None)
    cv.close()