import boto3
import os
import base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Espera en event['body']:
      {
        "bucket": "mi-bucket-123",
        "region": "us-east-1"   # opcional; default us-east-1
      }
    """
    body = event.get('body', {}) or {}
    bucket = body.get('bucket')
    region = body.get('region', 'us-east-1')

    if not bucket:
        return {"statusCode": 400, "error": "Falta 'bucket'."}

    try:
        s3 = boto3.client('s3', region_name=region)

        # En us-east-1 no se pasa CreateBucketConfiguration
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": region}
            )

        return {"statusCode": 200, "bucket": bucket, "region": region, "message": "Bucket creado."}

    except ClientError as e:
        return {"statusCode": 400, "error": str(e)}