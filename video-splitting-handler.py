import os
import subprocess
import boto3
# import logging
import json

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# os.chmod('/opt/bin/ffmpeg', 0o755)
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    # Loop through every file uploaded to the S3 bucket
    for record in event['Records']:
        input_bucket = record['s3']['bucket']['name']
        video_key = record['s3']['object']['key']
        download_path = '/tmp/' + video_key  # Temporary local path to download the video
        output_frame = os.path.splitext(video_key)[0] + '.jpg'
        upload_path = '/tmp/' + output_frame  # Temporary local path for the output frame
        
        if os.path.exists(upload_path):
            os.remove(upload_path)

        # Download the video file from S3 to the temporary local storage
        s3_client.download_file(Bucket=input_bucket, Key=video_key, Filename=download_path)

        # Command to extract a single frame using FFmpeg
        # split_cmd = 'ffmpeg -i ' + download_path + ' -vframes 1 ' + upload_path
        # logger.info("Starting FFmpeg processing")
        split_cmd = '/opt/bin/ffmpeg -i ' + download_path + ' -vframes 1 ' + upload_path
        try:
            subprocess.check_call(split_cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error code: {e.returncode}")
            print(f"Error output: {e.output}")
            return {
                'statusCode': 500,
                'body': 'Failed to process video'
            }

        # Upload the extracted frame to a specified S3 bucket
        output_bucket = '1225426618-stage-1'
        # logger.info(f"Uploading {output_frame} to {output_bucket}")
        s3_client.upload_file(Filename=upload_path, Bucket=output_bucket, Key=output_frame)
        # logger.info("Upload complete")
        
        invoke_response = lambda_client.invoke(
            FunctionName='face-recognition',
            InvocationType='Event',  # Asynchronous invocation
            Payload=json.dumps({
                'bucket_name': output_bucket,
                'image_file_name': output_frame
            })
        )
        # logger.info(f"Invoked face-recognition with response: {invoke_response}")

    return {
        'statusCode': 200,
        'body': 'Video processed and frame extracted successfully'
    }
