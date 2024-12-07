from fastapi import APIRouter


router = APIRouter(prefix='/admin')

@router.get("/teste")
async def teste_get():
    return {}