from minio.commonconfig import ComposeSource
from minio.deleteobjects import DeleteObject
import io
from utils import construct_name_of_file_part

def put_object(minio_client, bucket_name, filename, file_part_counter, chunk_buffer):
    minio_client.put_object(
        bucket_name=bucket_name,
        object_name=construct_name_of_file_part(filename, file_part_counter),
        data=io.BytesIO(chunk_buffer),
        length=len(chunk_buffer),
    )

def add_file_part_to_minio_arrays(bucket_name, sources, delete_objects, filename, file_part_counter):
    sources.append(ComposeSource(bucket_name, construct_name_of_file_part(filename, file_part_counter)))
    delete_objects.append(DeleteObject(construct_name_of_file_part(filename, file_part_counter)))