import ujson
import boto3
import time
import io
import os

s3 = boto3.client("s3")
bytes_buffer = io.BytesIO()


def lambda_handler(event, context):
    bucket = "aws-myhelsinki-data"

    key = 'myhelsinkidata.json'

    print(event)

    try:
        print("Downloading file.")
        start = time.time()
        response = s3.get_object(Bucket=bucket, Key=key)
        json_obj = response["Body"].read().decode("utf-8")
        end = time.time()
        print("Download file from S3", end - start)

        start = time.time()
        json_data = ujson.loads(json_obj)

        startIndex = event["queryStringParameters"]["startIndex"]
        endIndex = event["queryStringParameters"]["endIndex"]

        response = {
            "statusCode": 200,
            "headers": {},
            "body": ujson.dumps(json_data[int(startIndex):int(endIndex)])
        }
        end = time.time()
        print("Data to response", end - start)
        return response

    except Exception as e:
        raise e
