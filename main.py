from picamera import PiCamera
from time import sleep
import boto3
import json
from datetime import datetime

BucketName = ""

def take_pic(pic_name):
    camera =PiCamera()
    st=255
    camera.start_preview(alpha=st)
    sleep(5)
    camera.capture("./media/"+pic_name)
    camera.stop_preview()

def get_pic_name():
    return "image{}.jpg".format(str(datetime.now()))

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
if __name__ == "__main__":
    pic_name= get_pic_name()
    take_pic(pic_name)
    