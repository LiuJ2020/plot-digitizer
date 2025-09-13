from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import cv2
import numpy as np
import tempfile
import os

from ..utils.image_helpers import preprocess_image
from ..services.axis_detection import detect_axes

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Invalid file type.")
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        img = cv2.imread(tmp_path)
        if img is None:
            raise HTTPException(status_code=400, detail="Could not read image.")
        img = preprocess_image(img)
        axes_img, axes_data = detect_axes(img)
        # Save processed image for preview (optional)
        preview_path = tmp_path + "_axes.jpg"
        cv2.imwrite(preview_path, axes_img)
        os.remove(tmp_path)
        return JSONResponse({
            "axes_data": axes_data,
            "preview_path": preview_path
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
