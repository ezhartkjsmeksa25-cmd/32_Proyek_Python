import os
from PIL import Image

def process_image(input_path, output_path, target_format="JPEG", quality=85, resize_dim=None):
    with Image.open(input_path) as img:
        # Konversi otomatis RGBA/P ke RGB jika menyimpan sebagai JPEG
        if target_format.upper() in ["JPEG", "JPG"] and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Resize jika dimensi diberikan
        if resize_dim and isinstance(resize_dim, tuple):
            img = img.resize(resize_dim, Image.Resampling.LANCZOS)
        
        # Simpan sesuai format target
        if target_format.upper() in ["JPEG", "JPG"]:
            img.save(output_path, format="JPEG", quality=quality, optimize=True)
        else:
            img.save(output_path, format="PNG", optimize=True)