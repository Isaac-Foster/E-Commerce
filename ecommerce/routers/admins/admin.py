import os

from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix='/admin')


@router.get("/teste")
async def teste_get():
    return {"message": "Rota de teste funcionando"}


@router.post("/upload_midia")
async def upload_midia(file: UploadFile = File(...)):
    # Caminho onde você vai salvar os arquivos
    upload_dir = "dowloads/"

    # Garantir que o diretório exista
    os.makedirs(upload_dir, exist_ok=True)

    # Obter o nome do arquivo
    file_name = file.filename
    file_path = os.path.join(upload_dir, file_name)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {"message": "Arquivo enviado com sucesso", "file_name": file_name}

    except Exception as e:
        return {"message": f"Erro ao enviar arquivo: {str(e)}"}, 500
