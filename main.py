from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from repair import repair_stl
import os
import uuid

app = FastAPI()
UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_stl(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}_input.stl")
    output_path = os.path.join(UPLOAD_DIR, f"{file_id}_repaired.stl")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    repair_stl(input_path, output_path)

    return {"download_url": f"/download/{file_id}"}

@app.get("/download/{file_id}")
async def download(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_repaired.stl")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/sla", filename="repaired.stl")
    return {"error": "Datei nicht gefunden"}

