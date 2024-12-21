Para adicionar as funcionalidades que você mencionou, como **verificação de arquivos duplicados**, **listagem de arquivos** e **geração de links para o front-end** no seu código, podemos aprimorar o código de algumas maneiras. Abaixo estão as etapas sugeridas:

### 1. **Verificação de Arquivos Duplicados**
Você já tem uma verificação básica no método `upload`, mas podemos melhorar isso para verificar se o arquivo já existe no bucket com base no nome do arquivo, ou, alternativamente, criar um hash do conteúdo do arquivo (checksum) para garantir que não haja duplicatas, mesmo que o nome seja o mesmo.

### 2. **Método de Listagem de Arquivos**
Você já tem a função `get_all`, mas ela não fornece links para download direto. Podemos modificar isso para retornar URLs pré-assinadas de acesso direto.

### 3. **Geração de Links de Acesso para o Front-End**
Uma solução comum é usar URLs pré-assinadas que permitem acesso temporário aos objetos no bucket, sem precisar expor a chave de API diretamente no front-end.

### 4. **Atualização do Banco de Dados**
Você mencionou que cada produto pode ter várias fotos. Para isso, será necessário adicionar uma tabela de relacionamento no banco de dados para associar múltiplos arquivos a um único produto. Vou abordar isso posteriormente.

### **Alterações no Código**:

#### Modificando `StorageManager`:

1. **Verificação de Arquivos Duplicados (Baseado no Conteúdo)**

Podemos usar um hash MD5 ou SHA256 para gerar uma assinatura única do arquivo e verificar se ele já existe no bucket.

2. **Método para Listar Arquivos e Retornar Links**:

```python
import hashlib
from fastapi import HTTPException

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

        # Gerar hash do arquivo para verificar duplicidade
        file_hash = await self.generate_file_hash(file)

        # Verificar se o arquivo já existe no bucket (baseado no hash)
        if await self.check_if_file_exists(file_hash):
            raise HTTPException(status_code=400, detail="Arquivo duplicado.")

        try:
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

            # Salvar o hash associado ao id do arquivo no banco de dados (opcional)
            return File(_id, self.config)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao enviar arquivo: {str(e)}")

    async def generate_file_hash(self, file: UploadFile, chunk_size: int = 1024 * 1024):
        """Gera um hash único baseado no conteúdo do arquivo"""
        hash_md5 = hashlib.md5()
        content = await file.read()
        hash_md5.update(content)
        return hash_md5.hexdigest()

    async def check_if_file_exists(self, file_hash: str):
        """Verifica se o arquivo com o mesmo hash já existe no bucket"""
        objects = await self.get_all()
        for obj in objects:
            if obj.name == file_hash:  # Assume que o nome do arquivo no bucket é o hash
                return True
        return False

    async def get_all(self):
        # Listar todos os arquivos e gerar links públicos (ou pré-assinados)
        objects = await asyncio.to_thread(self.o.list_objects, self.namespace, self.bucket).data.objects
        file_urls = []
        for obj in objects:
            url = self.o.generate_presigned_url(self.namespace, self.bucket, obj.name, expiration_in_seconds=3600)
            file_urls.append({"file_id": obj.name, "url": url})
        return file_urls

    async def stream_file(self, name: str):
        try:
            response = await asyncio.to_thread(self.o.get_object, self.namespace, self.bucket, name)
            file_stream = BytesIO(response.data.content)
            return file_stream
        except Exception as e:
            print(f"Erro ao obter o arquivo: {str(e)}")
            return None

    async def download(self, name: str):
        # Baixando o arquivo em chunks de forma assíncrona
        response = await asyncio.to_thread(self.o.get_object, self.namespace, self.bucket, name)
        with open(f"downloads/{name}", 'wb') as f:
            for chunk in response.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(chunk)

    async def delete(self, file: File):
        try:
            await asyncio.to_thread(self.o.delete_object, self.namespace, self.bucket, file.id)
            return True
        except Exception:
            return False
```

### **Alterações no Código da Rota (FastAPI)**

Agora, a rota de upload pode gerar links para o front-end após o upload de um arquivo.

```python
@router.post("/upload_midia")
async def upload_midia(file: UploadFile = File(...)):
    # Tamanho do chunk
    chunk_size = 1024 * 1024

    try:
        # Realiza o upload e retorna o ID do arquivo
        result = await storage_manager.upload(file)
        
        # Obter todos os arquivos e gerar links para o front-end
        file_links = await storage_manager.get_all()
        
        # Filtra o link do arquivo recém-enviado
        file_url = next((item for item in file_links if item["file_id"] == result.id), None)
        
        if file_url:
            return {"message": "Arquivo enviado com sucesso", "file_url": file_url["url"]}
        else:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado após upload.")

    except Exception as e:
        return {"message": f"Erro ao enviar arquivo: {str(e)}"}, 500
```

### **Explicação das Modificações**:

1. **Geração de Hash para Arquivos**: Ao realizar o upload, o código gera um hash MD5 do arquivo. Esse hash é usado para verificar se o arquivo já existe no bucket. Se o hash já existir, o arquivo não será enviado novamente, evitando duplicação.
   
2. **Listagem de Arquivos**: A função `get_all` agora retorna links pré-assinados para os arquivos armazenados. Isso permite que você forneça links diretos para o front-end, com validade de 1 hora, por exemplo.

3. **Uso de URLs Pré-assinadas**: A função `generate_presigned_url` da SDK OCI é usada para gerar URLs temporárias para o acesso aos arquivos armazenados no bucket. Essa URL pode ser usada para acessar os arquivos diretamente sem expor as credenciais da API.

### **Banco de Dados**:

- Para armazenar os IDs dos arquivos, você pode ter uma tabela de `produtos` e uma tabela de `imagens_produto` que contenha o `product_id` e o `file_id` (que é o ID do arquivo no bucket).
  
  Exemplo de modelagem:
  
  ```sql
  CREATE TABLE produtos (
      id INT PRIMARY KEY,
      nome VARCHAR(255),
      descricao TEXT
  );

  CREATE TABLE imagens_produto (
      produto_id INT,
      file_id VARCHAR(255),  -- ID do arquivo no bucket
      PRIMARY KEY (produto_id, file_id),
      FOREIGN KEY (produto_id) REFERENCES produtos(id)
  );
  ```

Com essa estrutura, um produto pode ter várias imagens associadas, e você pode usar os links gerados pelo `StorageManager` para exibir as imagens no front-end.

### Conclusão

Com essas alterações, o seu sistema de gerenciamento de mídia usando o OCI (Oracle Cloud Infrastructure) será mais robusto, permitindo verificar duplicatas, listar arquivos com links para o front-end, e melhorar a eficiência no armazenamento e recuperação de mídias. Isso também facilita a integração com um banco de dados de produtos, caso você queira associar múltiplas imagens a um único produto.