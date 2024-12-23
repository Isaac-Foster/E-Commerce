from fastapi import UploadFile
from dataclasses import dataclass
from uuid import uuid4
import oci
import aiofiles
import asyncio
from io import BytesIO

@dataclass
class File:
    id: str
    account: str


@dataclass
class StorageManager:
    config: str
    bucket: str
    namespace: str = None
    o: oci.object_storage.ObjectStorageClient = None

    def __post_init__(self):
        # Criação do cliente OCI
        self.o = oci.object_storage.ObjectStorageClient(
            oci.config.from_file(
                f"config/media/oracle/{self.config}/{self.config}")
        )

        if self.namespace is None:
            self.namespace = self.o.get_namespace().data

    async def upload(self, file: UploadFile, chunk_size: int = 1024 * 1024):
        _id = str(uuid4()).replace("-", "")

        try:
            # Verifica se o arquivo já existe no bucket
            self.o.head_object(self.namespace, self.bucket, _id)
        except oci.exceptions.ServiceError as e:
            if e.status == 404: 
                # Lê o conteúdo do arquivo enviado
                file_content = await file.read()  # Lê todo o conteúdo do arquivo

                # Utiliza um BytesIO para simular um arquivo em memória
                with BytesIO(file_content) as f:
                    f.seek(0)
                    
                    while True:
                        # Lê em pedaços (chunks) do arquivo
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break 

                        self.o.put_object(
                            namespace_name=self.namespace,
                            bucket_name=self.bucket,
                            object_name=_id,
                            put_object_body=chunk
                        )

                return File(_id, self.config)

        return {"message": "Arquivo já existe no bucket."}

    async def get_all(self):
        # Realizando a operação de listagem de objetos de forma assíncrona
        return await asyncio.to_thread(
            self.o.list_objects, 
            self.namespace,
            self.bucket).data.objects

    async def stream_file(self, name: str):
        try:
            # Realizando operação de streaming assíncrona
            response = await asyncio.to_thread(
                self.o.get_object, 
                self.namespace, 
                self.bucket, 
                name)
            file_stream = BytesIO(response.data.content)
            return file_stream
        except Exception as e:
            print(f"Erro ao obter o arquivo: {str(e)}")
            return None

    async def download(self, name: str):
        # Baixando o arquivo em chunks de forma assíncrona
        response = await asyncio.to_thread(
            self.o.get_object, 
                self.namespace, 
                self.bucket, 
                name
            )

        with open(f"downloads/{name}", 'wb') as f:
            for chunk in response.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(chunk)

    async def delete(self, file: File):
        try:
            # Deletando o arquivo de forma assíncrona
            await asyncio.to_thread(
                self.o.delete_object, 
                self.namespace, 
                self.bucket, 
                file.id
            )
            return True
        except Exception:
            return False


storage_manager = StorageManager("base", "photos")
