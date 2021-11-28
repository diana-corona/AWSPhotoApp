import base64
import boto3
import json

s3 = boto3.client("s3")

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)

def download_image(event,bucket_name):
    image_name = event["queryStringParameters"]["file"]
    s3_image = s3.get_object(Bucket=bucket_name, Key=image_name)
    print(s3_image)
    file_content = s3_image["Body"].read()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/jpg",
            "Content-Disposition": "attachment; filename={}".format(image_name)
        },
        "body": base64.b64encode(file_content),
        "isBase64Encoded": True
    }

def upload_image(event,bucket_name):
    data = json.loads(event["body"])
    image_name = data["name"]
    image = data["file"]
    image = image[image.find(",")+1:]
    image_decoded = base64.b64decode(image + "===")
    s3.put_object(Bucket=bucket_name, Key=image_name, Body=image)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"message": "successfully inserted image"})
    }


def lambda_handler(event, context):
    bucket_name = "serverless-photo-app"
    if event["httpMethod"] == "GET" : 
        #bucket_name = event ["pathParameters"]["bucket"]
        return json.dumps(download_image(event,bucket_name), cls=JsonEncoder)
        
    if event["httpMethod"] == "POST" : 
        return upload_image(event,bucket_name)
        