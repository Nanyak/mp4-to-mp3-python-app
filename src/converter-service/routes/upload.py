from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from bson import ObjectId
import os
import shutil
from fastapi.responses import JSONResponse
os.makedirs("/tmp/uploads", exist_ok=True)
router = APIRouter(prefix = "/api/converter", tags=["converter"])
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = None):
    try:
        file_id = str(ObjectId())
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        stored_filename = f"{uuid.uuid4()}{file_extension}"
        saved_path = os.path.join("/tmp/uploads", stored_filename)

        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        metadata = {
            "_id": file_id,
            "user_id": user_id,
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "status": "pending",
            "saved_path": saved_path,
            "result_path": None,
        }

#        insert to mongo db
        job = {
            "file_id": file_id,
            "user_id": user_id,
            "saved_path": saved_path,
            "target_format": "mp3",
        }

#       send job to rabbitmq
        return JSONResponse(content={"file_id": file_id, "message": "File uploaded successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))