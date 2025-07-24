import json
import boto3
import os

s3_client = boto3.client('s3')
ses_client = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    # Get file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Email content
    subject = "New Video Uploaded"
    body = f"A new video has been uploaded:\n\nFile: {file_key}\nBucket: {bucket}\nS3 Path: s3://{bucket}/{file_key}"

    # Send email via SES
    ses_client.send_email(
        Source=os.environ['SOURCE_EMAIL'],
        Destination={'ToAddresses': [os.environ['DESTINATION_EMAIL']]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }
