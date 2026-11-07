import os
from PIL import Image, ImageDraw
import rembg

ARTIFACT_DIR = r"C:\Users\lenovo\.gemini\antigravity\brain\12a76aaf-79e8-4e6b-bbdd-50631224fa6f"
OUTPUT_DIR = r"C:\Users\lenovo\.gemini\antigravity\scratch\passport-photo-maker\static\assets\suits"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find generated files
images_to_process = {
    "men_suit_black": "suit_men_black_1794029199758.jpg",
    "men_suit_navy": "suit_men_navy_headless_1794029341001.jpg",
    "men_shirt_white": "shirt_men_white_1794029407506.jpg",
    "women_suit_black": "suit_women_black_1794029282523.jpg",
    "women_suit_navy": "suit_women_navy_1794029464529.jpg",
}

def clean_suit_cutout(img_path, output_name, neck_cut_box=None):
    print(f"Processing {output_name}...")
    full_path = os.path.join(ARTIFACT_DIR, img_path)
    img = Image.open(full_path)
    
    # 1. Remove background using rembg
    cutout = rembg.remove(img)
    
    # 2. If mannequin neck/head visible at top, erase it to make a clean neck opening
    w, h = cutout.size
    draw = ImageDraw.Draw(cutout)
    
    # Default neck cutout mask (removes mannequin neck cylinder above collar)
    # The mannequin neck is in top-center region
    if "men_suit_black" in output_name:
        # Cut chin/neck area
        cutout_mask = Image.new("L", (w, h), 255)
        m_draw = ImageDraw.Draw(cutout_mask)
        # Erase upper neck/chin
        m_draw.ellipse([w * 0.32, -h * 0.1, w * 0.68, h * 0.20], fill=0)
        cutout.putalpha(Image.composite(cutout.getchannel("A"), cutout_mask, cutout_mask))
    elif "men_suit_navy" in output_name:
        cutout_mask = Image.new("L", (w, h), 255)
        m_draw = ImageDraw.Draw(cutout_mask)
        m_draw.ellipse([w * 0.35, -h * 0.1, w * 0.65, h * 0.26], fill=0)
        cutout.putalpha(Image.composite(cutout.getchannel("A"), cutout_mask, cutout_mask))
    elif "men_shirt_white" in output_name:
        cutout_mask = Image.new("L", (w, h), 255)
        m_draw = ImageDraw.Draw(cutout_mask)
        m_draw.ellipse([w * 0.35, -h * 0.1, w * 0.65, h * 0.30], fill=0)
        cutout.putalpha(Image.composite(cutout.getchannel("A"), cutout_mask, cutout_mask))
    elif "women_suit_black" in output_name:
        cutout_mask = Image.new("L", (w, h), 255)
        m_draw = ImageDraw.Draw(cutout_mask)
        m_draw.ellipse([w * 0.35, -h * 0.1, w * 0.65, h * 0.24], fill=0)
        cutout.putalpha(Image.composite(cutout.getchannel("A"), cutout_mask, cutout_mask))
    elif "women_suit_navy" in output_name:
        cutout_mask = Image.new("L", (w, h), 255)
        m_draw = ImageDraw.Draw(cutout_mask)
        m_draw.ellipse([w * 0.35, -h * 0.1, w * 0.65, h * 0.28], fill=0)
        cutout.putalpha(Image.composite(cutout.getchannel("A"), cutout_mask, cutout_mask))

    # Resize to standard 800x800 for high performance & crisp rendering
    cutout = cutout.resize((800, 800), Image.Resampling.LANCZOS)
    
    out_file = os.path.join(OUTPUT_DIR, f"{output_name}.png")
    cutout.save(out_file, "PNG")
    print(f"  Saved -> {out_file}")

for name, filename in images_to_process.items():
    clean_suit_cutout(filename, name)

print("\nALL SUIT ASSETS PREPARED!")
