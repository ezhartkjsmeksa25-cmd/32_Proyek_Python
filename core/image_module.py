import os
from PIL import Image

def process_image(input_path, output_path, width=None, height=None, quality=85, target_format="JPEG"):
    """
    Mengubah format, meresize, dan mengompres ukuran file gambar.
    """
    with Image.open(input_path) as img:
        # Konversi RGBA ke RGB jika format tujuan adalah JPEG/JPG
        if target_format.upper() in ["JPEG", "JPG"] and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Ubah dimensi gambar jika parameter width & height diisi
        if width and height:
            img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
            
        # Simpan dengan tingkat kompresi kualitas
        img.save(output_path, format=target_format, quality=quality, optimize=True)
    return True