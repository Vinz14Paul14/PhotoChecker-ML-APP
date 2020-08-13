import boto3
from config import aws_access_key_id
from config import aws_secret_access_key
from config import s3_bucket
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
import S3handler
# from pathlib import Path

client=boto3.client('rekognition',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

def detect_faces(photo, bucket=s3_bucket):
    
    # load image from S3 bucket
    s3Response = S3handler.get_file(photo)
    stream = io.BytesIO(s3Response['Body'].read())
    content_type = s3Response['ContentType']
    image=Image.open(stream)

    # Call DetectFaces
    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])

    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)
    
    # for saving individual faces as files 
    # filestring = Path(photo)
    # filestem = filestring.stem
    # filesuffix = filestring.suffix

    font = ImageFont.truetype("arial.ttf", 20)
    index = 1
    # calculate and display bounding boxes for each detected face
    for faceDetail in response['FaceDetails']:
        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']

        points = (
            (left,top),
            (left + width, top),
            (left + width, top + height),
            (left , top + height),
            (left, top)
        )
        draw.line(points, fill='#00d400', width=2)  # green
        draw.text((left,top), str(index), fill="red", font=font)
        index += 1

        # Alternatively can draw rectangle. However you can't set line width.
        #draw.rectangle([left,top, left + width, top + height], outline='#00d400')

        # we could save individual faces as files in s3, but this is an expensive operation
        # To Do: crop the face and save as a separate file, add face1, face2 etc to file name
        # box = (left,top, left + width, top + height)
        # region = image.crop(box)

    # save the image to an in memory file
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format=image.format)
    in_mem_file.seek(0)

    # save image file back to S3 using the same filename
    S3handler.upload_file_to_s3(file=in_mem_file, filename=photo, content_type=content_type)
    return response

def recognize_celebrities(photo, bucket=s3_bucket):
    return client.recognize_celebrities(Image={'S3Object':{'Bucket':bucket,'Name':photo}})

def detect_labels(photo, bucket=s3_bucket):
    return client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MaxLabels=10, MinConfidence=0)

def detect_unsafeContent(photo, bucket=s3_bucket):
    return client.detect_moderation_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MinConfidence=50)

def main():
    import json
    # change photo to an image file name in s3_bucket
    photo='StarWars.jpg'
    data = detect_faces(photo)
    # print("Face data -------------------------------------")
    # print(json.dumps(data, indent=4, sort_keys=True))

    # data = recognize_celebrities(photo)
    # print("Celebrities data -------------------------------------")
    # print(json.dumps(data, indent=4, sort_keys=True))

    # data = detect_labels(photo)
    # print("Labels data -------------------------------------")
    # print(json.dumps(data, indent=4, sort_keys=True))

    # data = detect_unsafeContent(photo)
    # print("Unsafe data -------------------------------------")
    # print(json.dumps(data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()