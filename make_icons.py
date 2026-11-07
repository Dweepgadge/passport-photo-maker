import os
from PIL import Image, ImageDraw

ICONS_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\passport-photo-maker\static\assets\icons"
os.makedirs(ICONS_DIR, exist_ok=True)

def generate_icon(size):
    # Create gradient background
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background
    radius = int(size * 0.22)
    # Royal blue background
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=(37, 99, 235, 255))

    # Inner decorative subtle ring
    pad = int(size * 0.08)
    draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=int(radius * 0.7), outline=(255, 255, 255, 60), width=max(2, int(size * 0.015)))

    # Draw Camera / Portrait Silhouette Symbol
    head_cx = size // 2
    head_cy = int(size * 0.38)
    head_r = int(size * 0.16)
    draw.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r], fill=(255, 255, 255, 255))

    # Shoulders
    shoulder_w = int(size * 0.32)
    shoulder_top = int(size * 0.58)
    shoulder_bottom = int(size * 0.82)
    draw.chord([head_cx - shoulder_w, shoulder_top, head_cx + shoulder_w, shoulder_bottom + int(size * 0.1)], start=180, end=0, fill=(255, 255, 255, 255))

    # Collar / Tie accent
    tie_top = shoulder_top + int(size * 0.04)
    tie_w = int(size * 0.035)
    tie_bottom = shoulder_bottom - int(size * 0.04)
    draw.polygon([
        (head_cx - tie_w, tie_top),
        (head_cx + tie_w, tie_top),
        (head_cx + tie_w * 1.5, tie_bottom),
        (head_cx, tie_bottom + int(size * 0.04)),
        (head_cx - tie_w * 1.5, tie_bottom)
    ], fill=(30, 64, 175, 255))

    return img

icon192 = generate_icon(192)
icon192.save(os.path.join(ICONS_DIR, "icon-192.png"), "PNG")

icon512 = generate_icon(512)
icon512.save(os.path.join(ICONS_DIR, "icon-512.png"), "PNG")

print("Created icon-192.png and icon-512.png successfully!")
