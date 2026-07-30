from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController, ProcessController
from src.routes.schemas.data import ProcessRequest
import aiofiles
from src.models import ResponseSignal
import logging

logger = logging.getLogger("uvicorn.errors")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    #validate file properties
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename, 
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path,"wb") as f : 
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e :
        logger.error(f"Error While Uploading file : {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOADED_FAILED
            }
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCEES.value,
            "file_id": file_id
        }
    )

@data_router.post("/process/{project_id}")
async def procee_endpoint(project_id: str, process_request: ProcessRequest):
    
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0 : 
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value,
            }
        )

    return file_chunks