import os
from core.image_module import process_image

print("=== Pengujian Modul Gambar ===")
input_sample = "gambar.jpg" 
output_sample = "hasil_kompresi.jpg"

if os.path.exists(input_sample):
    process_image(input_sample, output_sample, quality=50, target_format="JPEG")
    print(f"Sukses! File berhasil diproses dan disimpan di: {output_sample}")
else:
    print(f"Peringatan: Sediakan file '{input_sample}' di folder proyek.")