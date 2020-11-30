import ujson
import requests
import boto3
from datetime import datetime

s3 = boto3.client("s3")

def lambda_handler(event, context):

    bucket = "aws-myhelsinki-data"

    data = requests.get("http://open-api.myhelsinki.fi/v1/events/").json()

    today = datetime.today().isoformat()

    sorted_data = sorted((x for x in data["data"] if x["event_dates"]["starting_day"] is not None and x["event_dates"]["starting_day"] > today ),key=lambda x: x["event_dates"]["starting_day"])

    fileName = "myhelsinkidata" + ".json"
    uploadByteStream = bytes(ujson.dumps(sorted_data).encode("UTF-8"))
    s3.put_object(Bucket=bucket, Key=fileName, Body=uploadByteStream)
    print("Put Complete ")