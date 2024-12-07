from fastapi import APIRouter


router = APIRouter(prefix='/users')

@router.get("/teste")
async def teste_get_users():
    return {}