from dataclasses import dataclass
from uuid import uuid4

import oci


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
        self.o = oci.object_storage.ObjectStorageClient(
            oci.config.from_file(
                "config/media/oracle{}/{}".format(self.config, self.config))
            )

        if self.namespace is None:
            self.namespace = self.o.get_namespace().data


    def upload(self, file):
        while True:
            _id = str(uuid4()).replace("-","")

            try:
                a = self.o.head_object(self.namespace, self.bucket, _id)
            except Exception:
                with open(f"downloads/{file}", "rb") as f:
                    self.o.put_object(
                        namespace_name=self.namespace,
                        bucket_name=self.bucket,
                        object_name=_id,
                        put_object_body=f
                    )

                return File(_id, self.config)


    def get_all(self):
        objects = self.o.list_objects(
            namespace_name=self.namespace,
            bucket_name=self.buckets
        ).data.objects

        return objects


    def stream_file(self, name: str):
        try:
            response = self.o.get_object(self.namespace, self.bucket, name)

            file_stream = io.BytesIO(response.data.content)
            return file_stream
        except Exception as e:
            print(f"Erro ao obter o arquivo: {str(e)}")
            return None


    def download(self, name):
       response = self.o.get_object(self.name, self.bucket, name)
       with open("downloads/{name}", 'wb') as f:
            for chunk in response.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(chunk)


    def delete(self, file: File):
        try:
            a = self.o.head_object(self.namespace, self.bucket, _id)
            self.o.delete_object(self.namespace, self.bucket, file.id)
            return True
        except Exception:
            return False


base = Storage("base", "photos")
print(base.o)
