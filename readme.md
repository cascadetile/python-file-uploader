I choosed FastAPI because all of its endpoints are async which is good for simultaneous upload from miltiple clients.

Then I've read this answer https://stackoverflow.com/a/73443824 and found out that standard FileUpload of FastAPI is saving files to disk if it's bigger than 1MB. Which is not suitable for my task because it needs to upload >1.5GB files while running on 512MB disk space machine. That's why I decided to use request.stream(). It gives you an ability to read incoming requests without waiting until it's fully received.

Set Access Key and Secret Key in docker-compose envs
Run docker-compose up
Create a bucket called "my-bucket" or you can name it as you wish, but in that case rename bucket_name variable in docker-compose

Files are uploaded to Minio as separate 5MB files and then combined into one on Minio's side. After that these separate files are cleared. put_object is supposed to do last 2 steps itself but for some reason it just records only latest part of a file. So that's why I did it this way

Also no validation because I'm new in Python and don't have much time for this task

Minio Python API (poorly documented IMO): https://min.io/docs/minio/linux/developers/python/API.html
Starlette request API (FastAPI inherits from it): https://www.starlette.io/requests/
Also this GitHub issue about streams in FastAPI was helpful: https://github.com/tiangolo/fastapi/issues/58
Minio container: https://github.com/minio/minio/blob/master/docs/docker/README.md