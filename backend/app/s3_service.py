import boto3
import json

# -----------------------------
# S3 CONFIG
# -----------------------------
BUCKET_NAME = "energy-forecast-unstuck-2026"

# Initialize S3 client
s3 = boto3.client("s3")


# ---------------------------------------------------
# Upload file-like object to S3
# ---------------------------------------------------
def upload_file_to_s3(file_obj, key: str):
    """
    Uploads a file-like object (BytesIO or UploadFile.file)
    to the specified S3 key.
    """
    s3.upload_fileobj(file_obj, BUCKET_NAME, key)

    return f"s3://{BUCKET_NAME}/{key}"


# ---------------------------------------------------
# Upload JSON data to S3
# ---------------------------------------------------
def upload_json_to_s3(data: dict, key: str):
    """
    Uploads JSON data to S3.
    """
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json"
    )

    return f"s3://{BUCKET_NAME}/{key}"


# ---------------------------------------------------
# Download raw file from S3
# ---------------------------------------------------
def download_file_from_s3(key: str):
    """
    Downloads a file from S3 and returns raw bytes.
    """
    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    return obj["Body"].read()


# ---------------------------------------------------
# Fetch JSON file from S3
# ---------------------------------------------------
def get_json_from_s3(key: str):
    """
    Fetch JSON content from S3 and return as Python dict.
    """
    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    data = json.loads(
        obj["Body"].read().decode("utf-8")
    )

    return data

# import boto3 --worked till now
# import json

# BUCKET_NAME = "energy-forecast-unstuck-2026"

# s3_client = boto3.client("s3")


# def upload_file_to_s3(local_path, s3_key):
#     s3_client.upload_file(local_path, BUCKET_NAME, s3_key)
#     return f"s3://{BUCKET_NAME}/{s3_key}"


# def upload_json_to_s3(data: dict, s3_key: str):
#     s3_client.put_object(
#         Bucket=BUCKET_NAME,
#         Key=s3_key,
#         Body=json.dumps(data),
#         ContentType="application/json"
#     )
#     return f"s3://{BUCKET_NAME}/{s3_key}"
# import boto3
# import json

# BUCKET_NAME = "energy-forecast-unstuck-2026"

# s3 = boto3.client("s3")


# def upload_file_to_s3(file_obj, key):
#     s3.upload_fileobj(file_obj, BUCKET_NAME, key)


# def upload_json_to_s3(data, key):
#     s3.put_object(
#         Bucket=BUCKET_NAME,
#         Key=key,
#         Body=json.dumps(data, indent=2),
#         ContentType="application/json"
#     )


# def download_file_from_s3(key):
#     obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
#     return obj["Body"].read()
# import boto3
# import json
# import os

# s3 = boto3.client("s3")

# BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# def upload_file_to_s3(file_obj, s3_key: str):
#     """
#     Uploads file-like object to S3.
#     """
#     s3.upload_fileobj(file_obj, BUCKET_NAME, s3_key)
#     return f"s3://{BUCKET_NAME}/{s3_key}"


# def upload_json_to_s3(data: dict, s3_key: str):
#     """
#     Uploads JSON data to S3.
#     """
#     s3.put_object(
#         Bucket=BUCKET_NAME,
#         Key=s3_key,
#         Body=json.dumps(data, indent=2),
#         ContentType="application/json"
#     )
#     return f"s3://{BUCKET_NAME}/{s3_key}"