# AWS Lambda-based Video Analysis Application
This project demonstrates the creation of a scalable, serverless video analysis application using AWS Lambda and other AWS services. The application processes videos by splitting them into frames, recognizes faces in the frames, and identifies individuals using a pre-trained neural network model.

## Project Summary
The application uses a multi-stage pipeline implemented with AWS Lambda functions to handle video files uploaded by users. It starts with a video being uploaded to an S3 bucket, followed by several stages of processing including video splitting, face detection, and face recognition.

## Architecture


## Key Components
### Input Bucket
Stores videos uploaded by the workload generator.

### Stage-1 Bucket
Stores the result of the video-splitting function.

### Output Bucket
Stores the result of the face-recognition function.

## Functions
Video-Splitting Function: Splits the uploaded video into frames.
Face-Recognition Function: Processes the frames to recognize and identify faces.

## Setup and Deployment
### Prerequisites
AWS account
AWS CLI configured on your machine
Knowledge of AWS Lambda, S3, and IAM permissions

### Deployment Steps
Create the necessary S3 buckets according to the naming conventions.
Deploy the Lambda functions using the AWS Management Console or CLI.
Set up the trigger for the video-splitting function on the input bucket.
Ensure IAM roles and policies are properly configured for access between services.
