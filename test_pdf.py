import os
from pypdf import PdfWriter
from core.pdf_module import merge_pdfs, split_pdf, pdf_to_docx

def create_sample_pdf(filename, num_pages=3):
    """Fungsi pembantu untuk membuat file PDF sampel."""
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=300, height=300)
    with open(filename, "wb") as f:
        writer.write(f)

def run_test():
    print("=== MEMULAI PENGUJIAN MODUL PDF ===")
    
    # 1. Buat PDF sampel
    print("[1/4] Membuat file PDF sampel untuk tes...")
    create_sample_pdf("sample1.pdf", num_pages=2)
    create_sample_pdf("sample2.pdf", num_pages=2)
    
    # 2. Tes Gabung PDF (Merge)
    print("[2/4] Menguji penggabungan PDF (Merge)...")
    merge_pdfs(["sample1.pdf", "sample2.pdf"], "hasil_merge.pdf")
    print("    -> Berhasil! Output: hasil_merge.pdf")
    
    # 3. Tes Pisah PDF (Split)
    print("[3/4] Menguji pemisahan PDF (Split)...")
    split_pdf("hasil_merge.pdf", "hasil_split.pdf", start_page=1, end_page=2)
    print("    -> Berhasil! Output: hasil_split.pdf")
    
    # 4. Tes Konversi PDF ke Word
    print("[4/4] Menguji konversi PDF ke DOCX...")
    pdf_to_docx("hasil_split.pdf", "hasil_konversi.docx")
    print("    -> Berhasil! Output: hasil_konversi.docx")
    
    print("\n=== SEMUA PENGUJIAN PDF SUKSES! ===")

if __name__ == "__main__":
    run_test()