import os
from PIL import Image

def process_image(input_path, output_path, target_format="JPEG", quality=85, resize_dim=None):
    """
    Memproses gambar: kompresi, konversi format, dan resize opsional.
    """
    with Image.open(input_path) as img:
        # Konversi mode warna ke RGB jika target JPEG (mencegah error gambar PNG transparan)
        if target_format.upper() in ["JPEG", "JPG"] and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Eksekusi Resize jika parameter diberikan
        if resize_dim and isinstance(resize_dim, tuple):
            img = img.resize(resize_dim, Image.Resampling.LANCZOS)
        
        # Simpan Gambar
        if target_format.upper() in ["JPEG", "JPG"]:
            img.save(output_path, format="JPEG", quality=quality, optimize=True)
        else:
            img.save(output_path, format="PNG", optimize=True)