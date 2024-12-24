import os

from fastapi import APIRouter, File, UploadFile

from ecommerce.database.storage import storage_manager

router = APIRouter(prefix='/admin', tags=["admin"])


@router.get("/teste")
async def teste_get():
    return {"message": "Rota de teste funcionando"}


@router.post("/upload_midia")
async def upload_midia(file: UploadFile = File(...)):
    file_name = file.filename
    file_path = os.path.join(path, file_name)
    chunk_size = 1024 * 1024 

    try:
        result = await storage_manager.upload(file, chunk_size)
        return {"message": "file upated sucessfull", "file_id": result.id}
    except Exception as e:
        return {"message": f"Erro update your file"}, 500
