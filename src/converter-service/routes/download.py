from fastapi import APIRouter
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/api/converter", tags=["converter"])

@router.get("/download")
async def download_file():
    try:
        return {"message": "Download endpoint is under construction"}
    except Exception as e:
        raise JSONResponse(content={"error": str(e)}, status_code=500)