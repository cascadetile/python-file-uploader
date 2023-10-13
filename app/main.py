import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from minio.error import S3Error
from starlette.requests import Request
from utils import get_current_timestamp
from utils import extract_file_format_from_headers
from utils import extract_filename_from_headers
from utils import remove_headers
from minio_utils import add_file_part_to_minio_arrays
from minio_utils import put_object

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

minio_client = Minio(
    "minio:9000",
    access_key=os.environ['MINIO_ACCESS_KEY'],
    secret_key=os.environ['MINIO_SECRET_KEY'],
    secure=False,
)

batch_size = 5 * 1024 * 1024  # 5MB
bucket_name = "my-bucket"

@app.post("/files/")
async def create_file(request: Request):
    filename = "default_filename" + str(get_current_timestamp())
    file_part_counter = 1
    total_bytes_read = 0

    file_format = ""
    
    sources = []
    delete_objects = []

    chunk_buffer = b''

    is_first_chunk = True

    async for chunk in request.stream():
        if is_first_chunk:
            filename = extract_filename_from_headers(chunk)
            if not filename:
                filename = "default_filename" + str(get_current_timestamp())
            else:
                filename += str(get_current_timestamp())
            file_format = extract_file_format_from_headers(chunk)
            chunk = remove_headers(chunk)
            is_first_chunk = False

        chunk_buffer += chunk
        total_bytes_read += len(chunk)

        if total_bytes_read >= batch_size:
            try:
                put_object(minio_client, bucket_name, filename, file_part_counter, chunk_buffer)

                add_file_part_to_minio_arrays(bucket_name, sources, delete_objects, filename, file_part_counter)

                chunk_buffer = b''
                total_bytes_read = 0
                file_part_counter += 1
            except S3Error as e:
                return {"error": f"Minio error: {str(e)}"}

    if total_bytes_read > 0:
        try:
            put_object(minio_client, bucket_name, filename, file_part_counter, chunk_buffer)

            add_file_part_to_minio_arrays(bucket_name, sources, delete_objects, filename, file_part_counter)
        except S3Error as e:
            return {"error": f"Minio error: {str(e)}"}

    try:
        result = minio_client.compose_object(bucket_name, filename + "." + file_format, sources)
        print(result.object_name, result.version_id)
    except S3Error as e:
        return {"error": f"Minio error: {str(e)}"}
    
    errors = minio_client.remove_objects(bucket_name, delete_objects)
    for error in errors:
        print("error occurred when deleting object", error)

    return {"message": "File uploaded successfully"}