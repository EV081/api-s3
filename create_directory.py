import boto3
import os
import base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Espera en event['body']:
      {
        "bucket": "mi-bucket-123",
        "prefix": "carpeta/subcarpeta/"  # si no termina en '/', se agrega
      }
    """
    body = event.get('body', {}) or {}
    bucket = body.get('bucket')
    prefix = body.get('prefix')

    if not bucket or not prefix:
        return {"statusCode": 400, "error": "Faltan 'bucket' y/o 'prefix'."}

    # asegurar que termine en '/'
    if not prefix.endswith('/'):
        prefix = prefix + '/'

    try:
        s3 = boto3.client('s3')
        # Objeto vacío para materializar el "directorio"
        s3.put_object(Bucket=bucket, Key=prefix, Body=b'')
        return {"statusCode": 200, "bucket": bucket, "prefix": prefix, "message": "Directorio creado."}
    except ClientError as e:
        return {"statusCode": 400, "error": str(e)}
