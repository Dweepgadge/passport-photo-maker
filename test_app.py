import io
import base64
from PIL import Image, ImageDraw
from presets import PRESETS, SHEET_PRESETS
import image_processor


def test_presets():
    print("Testing Presets...")
    assert "us_passport" in PRESETS
    assert "in_passport" in PRESETS
    assert "eu_schengen" in PRESETS
    assert "uk_passport" in PRESETS
    assert "ca_passport" in PRESETS
    print(f"  Passed! Found {len(PRESETS)} official presets and {len(SHEET_PRESETS)} sheet formats.")


def test_image_processing():
    print("Testing Image Processing & 300 DPI Export...")
    # Create synthetic test portrait
    img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw simple avatar shape
    draw.ellipse([100, 50, 300, 250], fill=(220, 180, 140, 255))  # Face
    draw.rectangle([80, 240, 320, 400], fill=(50, 80, 160, 255))  # Shirt

    # Test composite background
    white_bg = image_processor.composite_background(img, "#FFFFFF")
    assert white_bg.size == (400, 400)
    assert white_bg.mode == "RGB"
    # Corner should be pure white
    assert white_bg.getpixel((10, 10)) == (255, 255, 255)
    print("  Passed composite background!")

    # Test process_final_photo
    final_photo = image_processor.process_final_photo(
        white_bg, crop_box=(50, 30, 350, 370), target_width_px=600, target_height_px=600, dpi=300
    )
    assert final_photo.size == (600, 600)
    print("  Passed final photo resizing (600x600 px @ 300 DPI)!")

    # Test create_printable_sheet (4x6 @ 300 DPI = 1800 x 1200 px)
    sheet = image_processor.create_printable_sheet(final_photo, paper_format="4x6", dpi=300, max_copies=6)
    assert sheet.size == (1800, 1200)
    assert sheet.mode == "RGB"
    print("  Passed 4x6 inch printable sheet generation (1800x1200 px @ 300 DPI)!")

    # Test create_printable_sheet (A4 @ 300 DPI = 2480 x 3508 px)
    sheet_a4 = image_processor.create_printable_sheet(final_photo, paper_format="a4", dpi=300, max_copies=8)
    assert sheet_a4.size == (2480, 3508)
    print("  Passed A4 printable sheet generation (2480x3508 px @ 300 DPI)!")


def test_suits():
    print("Testing Suit Asset Library & Alpha Blending...")
    import os
    suits_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\passport-photo-maker\static\assets\suits"
    expected = [
        "men_suit_black.png",
        "men_suit_navy.png",
        "men_shirt_white.png",
        "women_suit_black.png",
        "women_suit_navy.png",
    ]
    for s in expected:
        p = os.path.join(suits_dir, s)
        assert os.path.exists(p), f"Missing suit: {s}"
        img = Image.open(p)
        assert img.mode == "RGBA"
        assert img.size == (800, 800)
    print(f"  Passed! Verified all {len(expected)} transparent suit overlays (800x800 RGBA).")


def test_payments_and_watermark():
    print("Testing Payments & Watermark Engine...")
    import payments
    
    # Test plans
    assert "single" in payments.PLANS
    assert "bundle" in payments.PLANS
    assert payments.PLANS["single"]["price_inr"] == 49
    assert payments.PLANS["bundle"]["price_inr"] == 99
    
    # Test order creation
    order = payments.create_order("bundle")
    assert order["order_id"].startswith("order_")
    assert order["amount"] == 9900
    print("  Passed order creation!")
    
    # Test payment verification & token issuance
    verif = payments.verify_payment(order["order_id"], "pay_test123", plan_id="bundle")
    assert verif["success"] is True
    assert payments.is_token_valid(verif["token"]) is True
    print("  Passed payment verification & authorization token!")
    
    # Test watermark application
    base_img = Image.new("RGB", (600, 600), (255, 255, 255))
    watermarked = image_processor.apply_watermark(base_img)
    assert watermarked.size == (600, 600)
    # Check that watermark modified some pixels (not purely white)
    assert watermarked.tobytes() != base_img.tobytes()
    print("  Passed preview watermark application!")


if __name__ == "__main__":
    test_presets()
    test_image_processing()
    test_suits()
    test_payments_and_watermark()
    print("\nALL AUTOMATED TESTS PASSED!")
