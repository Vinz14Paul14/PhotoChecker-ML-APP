from config import aws_access_key_id
from config import aws_secret_access_key
from config import s3_bucket
import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)


def upload_file_to_s3(file, filename, content_type, bucket_name=s3_bucket, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return f"https://{bucket_name}.s3.amazonaws.com/{filename}"

def get_file(filename, bucket_name=s3_bucket):
    response = s3.get_object(Bucket=bucket_name, Key=filename)
    return response
