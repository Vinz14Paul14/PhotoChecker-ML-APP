import boto3
from config import aws_access_key_id
from config import aws_secret_access_key
from config import s3_bucket

client=boto3.client('rekognition',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

def detect_faces(photo, bucket=s3_bucket):
    return client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])

def recognize_celebrities(photo, bucket=s3_bucket):
    return client.recognize_celebrities(Image={'S3Object':{'Bucket':bucket,'Name':photo}})

def detect_labels(photo, bucket=s3_bucket):
    return client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MaxLabels=10, MinConfidence=0)

def main():
    import json
    # change photo to an image file name in s3_bucket
    photo='StarWars.jpg'
    data = detect_faces(photo)
    print("Face data -------------------------------------")
    print(json.dumps(data, indent=4, sort_keys=True))

    data = recognize_celebrities(photo)
    print("Celebrities data -------------------------------------")
    print(json.dumps(data, indent=4, sort_keys=True))

    data = detect_labels(photo)
    print("Labels data -------------------------------------")
    print(json.dumps(data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()