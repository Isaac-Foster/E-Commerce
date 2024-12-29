import os

from fastapi import APIRouter, File, UploadFile

from ecommerce.infrastructure.database.storage import storage_manager

router = APIRouter(prefix='/admin', tags=["admin"])


@router.post("/product")
async def teste_get(data: dict):
    return {"message": "Rota de teste funcionando"}

