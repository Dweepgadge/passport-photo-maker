import io
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageColor
import numpy as np

try:
    from rembg import remove as rembg_remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False


def remove_background(image_bytes: bytes) -> Image.Image:
    """
    Remove background from an image using rembg, returning an RGBA PIL Image.
    If rembg is not installed, returns the original image in RGBA.
    """
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    if REMBG_AVAILABLE:
        output_image = rembg_remove(input_image)
        return output_image
    return input_image


def composite_background(rgba_image: Image.Image, hex_color: str = "#FFFFFF") -> Image.Image:
    """
    Composite an RGBA image onto a solid background color.
    Returns RGB image.
    """
    if rgba_image.mode != "RGBA":
        rgba_image = rgba_image.convert("RGBA")

    bg_rgb = ImageColor.getrgb(hex_color)
    background = Image.new("RGBA", rgba_image.size, bg_rgb + (255,))
    composed = Image.alpha_composite(background, rgba_image)
    return composed.convert("RGB")


def process_final_photo(
    image: Image.Image,
    crop_box: Optional[Tuple[int, int, int, int]] = None,
    target_width_px: int = 600,
    target_height_px: int = 600,
    dpi: int = 300,
) -> Image.Image:
    """
    Crop the image according to bounding box (left, top, right, bottom)
    and resize using Lanczos high-quality resampling with 300 DPI metadata.
    """
    if crop_box:
        left, top, right, bottom = crop_box
        # Clamp to bounds
        left = max(0, min(image.width - 1, left))
        top = max(0, min(image.height - 1, top))
        right = max(left + 1, min(image.width, right))
        bottom = max(top + 1, min(image.height, bottom))
        image = image.crop((left, top, right, bottom))

    resized = image.resize((target_width_px, target_height_px), Image.Resampling.LANCZOS)
    return resized


def create_printable_sheet(
    single_photo: Image.Image,
    paper_format: str = "4x6",
    dpi: int = 300,
    max_copies: int = 8,
) -> Image.Image:
    """
    Create a 300 DPI printable sheet (4x6 photo paper or A4) with cut guidelines.
    """
    if paper_format == "4x6":
        # 6x4 inch landscape: 1800 x 1200 px at 300 DPI
        sheet_w = 1800
        sheet_h = 1200
    elif paper_format == "a4":
        # A4 portrait: 2480 x 3508 px at 300 DPI
        sheet_w = 2480
        sheet_h = 3508
    else:
        sheet_w = 1800
        sheet_h = 1200

    photo_w, photo_h = single_photo.size

    # Spacing and margin
    gap_x = int(0.12 * dpi)  # ~3mm gap
    gap_y = int(0.12 * dpi)
    margin_min = int(0.2 * dpi)

    # Calculate how many photos can fit
    cols = max(1, (sheet_w - 2 * margin_min + gap_x) // (photo_w + gap_x))
    rows = max(1, (sheet_h - 2 * margin_min + gap_y) // (photo_h + gap_y))

    total_slots = cols * rows
    copies_to_draw = min(total_slots, max_copies)

    # Calculate actual grid dimensions and center it
    actual_grid_w = cols * photo_w + (cols - 1) * gap_x
    actual_grid_h = rows * photo_h + (rows - 1) * gap_y
    start_x = (sheet_w - actual_grid_w) // 2
    start_y = (sheet_h - actual_grid_h) // 2

    # Create white canvas
    sheet = Image.new("RGB", (sheet_w, sheet_h), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if count >= copies_to_draw:
                break
            x = start_x + c * (photo_w + gap_x)
            y = start_y + r * (photo_h + gap_y)

            sheet.paste(single_photo, (x, y))

            # Draw thin subtle cutting guide line around each photo
            draw.rectangle(
                [x - 1, y - 1, x + photo_w, y + photo_h],
                outline=(210, 215, 220),
                width=1,
            )

            # Draw small corner tick marks for scissors/guillotine cutting
            tick_len = int(0.08 * dpi)  # ~2mm
            # Top-left corner tick
            draw.line([(x - tick_len, y), (x + tick_len, y)], fill=(160, 165, 170), width=1)
            draw.line([(x, y - tick_len), (x, y + tick_len)], fill=(160, 165, 170), width=1)
            # Bottom-right corner tick
            draw.line([(x + photo_w - tick_len, y + photo_h), (x + photo_w + tick_len, y + photo_h)], fill=(160, 165, 170), width=1)
            draw.line([(x + photo_w, y + photo_h - tick_len), (x + photo_w, y + photo_h + tick_len)], fill=(160, 165, 170), width=1)

            count += 1
        if count >= copies_to_draw:
            break

    # Add small footer text
    footer_text = f"Official Passport/ID Photo Sheet • {paper_format.upper()} @ 300 DPI • Print at 100% scale (Do Not Scale / Fit to Page)"
    draw.text((start_x, sheet_h - int(0.15 * dpi)), footer_text, fill=(160, 165, 170))

    return sheet


def apply_watermark(image: Image.Image, text: str = "PASSPORTAI • PREVIEW") -> Image.Image:
    """
    Applies a semi-transparent diagonal watermark pattern over the image for free preview mode.
    """
    rgba = image.convert("RGBA")
    txt_layer = Image.new("RGBA", rgba.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt_layer)

    w, h = rgba.size

    # Step through image and draw watermark markers
    step_x = max(120, int(w * 0.45))
    step_y = max(80, int(h * 0.25))

    for y in range(0, h + step_y, step_y):
        for x in range(0, w + step_x, step_x):
            d.text((x + 10, y + 10), text, fill=(15, 23, 42, 65))

    watermarked = Image.alpha_composite(rgba, txt_layer)
    return watermarked.convert("RGB")

