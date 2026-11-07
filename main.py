import io
import base64
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from PIL import Image

from presets import PRESETS, SHEET_PRESETS
import image_processor
import payments

app = FastAPI(title="AI Official ID & Passport Photo Maker")


@app.get("/api/presets")
def get_presets():
    return {
        "presets": list(PRESETS.values()),
        "sheet_presets": list(SHEET_PRESETS.values()),
    }


@app.get("/api/plans")
def get_plans():
    return {
        "plans": list(payments.PLANS.values()),
        "is_test_mode": payments.IS_TEST_MODE,
        "razorpay_key": payments.RAZORPAY_KEY_ID,
    }


@app.post("/api/create-order")
def api_create_order(plan_id: str = Form("bundle")):
    return payments.create_order(plan_id)


@app.post("/api/verify-payment")
def api_verify_payment(
    order_id: str = Form(...),
    payment_id: str = Form(...),
    signature: Optional[str] = Form(None),
    plan_id: str = Form("bundle"),
):
    return payments.verify_payment(order_id, payment_id, signature, plan_id)


@app.post("/api/remove-bg")
async def api_remove_bg(file: UploadFile = File(...)):
    """
    Accepts an uploaded image and returns a transparent PNG (base64 data URL)
    with the background removed.
    """
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file uploaded.")

        cutout = image_processor.remove_background(content)

        buffered = io.BytesIO()
        cutout.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "success": True,
            "width": cutout.width,
            "height": cutout.height,
            "data_url": f"data:image/png;base64,{img_str}",
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.post("/api/process-photo")
async def api_process_photo(
    image_data: str = Form(...),
    preset_id: str = Form("us_passport"),
    bg_color: str = Form("#FFFFFF"),
    crop_x: int = Form(0),
    crop_y: int = Form(0),
    crop_width: int = Form(600),
    crop_height: int = Form(600),
    target_width_px: Optional[int] = Form(None),
    target_height_px: Optional[int] = Form(None),
    token: Optional[str] = Form(None),
):
    """
    Processes final cropped portrait with selected background color and DPI/pixel dimensions.
    Returns base64 data URL of the final photo (watermarked if unpaid).
    """
    try:
        # Decode base64 data URL
        if "," in image_data:
            _, encoded = image_data.split(",", 1)
        else:
            encoded = image_data
        image_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(image_bytes))

        # Determine dimensions
        if preset_id in PRESETS:
            preset = PRESETS[preset_id]
            tw = preset["width_px"]
            th = preset["height_px"]
            dpi = preset.get("dpi", 300)
        else:
            tw = target_width_px or 600
            th = target_height_px or 600
            dpi = 300

        # Composite background if image is transparent
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            final_rgb = image_processor.composite_background(img, bg_color)
        else:
            final_rgb = img.convert("RGB")

        # Crop and resize
        crop_box = (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height)
        result = image_processor.process_final_photo(
            final_rgb, crop_box=crop_box, target_width_px=tw, target_height_px=th, dpi=dpi
        )

        # Apply watermark if unpaid token
        is_paid = payments.is_token_valid(token) if token else False
        export_img = result if is_paid else image_processor.apply_watermark(result)

        buffered = io.BytesIO()
        export_img.save(buffered, format="JPEG", quality=95, dpi=(dpi, dpi))
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "success": True,
            "width": tw,
            "height": th,
            "dpi": dpi,
            "is_paid": is_paid,
            "data_url": f"data:image/jpeg;base64,{img_str}",
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.post("/api/generate-sheet")
async def api_generate_sheet(
    image_data: str = Form(...),
    paper_format: str = Form("4x6"),
    copies: int = Form(6),
    dpi: int = Form(300),
    token: Optional[str] = Form(None),
):
    """
    Generates a print-ready 4x6" or A4 sheet with multiple copies and cut lines.
    Watermarked unless valid payment token provided.
    """
    try:
        if "," in image_data:
            _, encoded = image_data.split(",", 1)
        else:
            encoded = image_data
        image_bytes = base64.b64decode(encoded)
        single_photo = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        sheet = image_processor.create_printable_sheet(
            single_photo, paper_format=paper_format, dpi=dpi, max_copies=copies
        )

        is_paid = payments.is_token_valid(token) if token else False
        export_sheet = sheet if is_paid else image_processor.apply_watermark(sheet)

        buffered = io.BytesIO()
        export_sheet.save(buffered, format="JPEG", quality=95, dpi=(dpi, dpi))
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "success": True,
            "width": sheet.width,
            "height": sheet.height,
            "dpi": dpi,
            "paper_format": paper_format,
            "is_paid": is_paid,
            "data_url": f"data:image/jpeg;base64,{img_str}",
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")
