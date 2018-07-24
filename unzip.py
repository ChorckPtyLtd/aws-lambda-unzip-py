from __future__ import print_function

import urllib
import zipfile
import boto3
import io
import json
import os

s3 = boto3.client('s3')
bucket = ''

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    status = message['av-status']
    key = urllib.unquote_plus(message['key'])
    bucket = message['bucket']
    path = os.path.dirname(key)
    if status == 'CLEAN':
        try:
            obj = s3.get_object(Bucket=bucket, Key=key)
            putObjects = []
            with io.BytesIO(obj["Body"].read()) as tf:
                # rewind the file
                tf.seek(0)
    
                # Read the file as a zipfile and process the members
                with zipfile.ZipFile(tf, mode='r') as zipf:
                    for file in zipf.infolist():
                        fileName = os.path.join(path, file.filename)
                        putFile = s3.put_object(Bucket=bucket, Key=fileName, Body=zipf.read(file))
                        putObjects.append(putFile)
    
    
            # Delete zip file after unzip
            if len(putObjects) > 0:
                deletedObj = s3.delete_object(Bucket=bucket, Key=key)
    
        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
            raise e