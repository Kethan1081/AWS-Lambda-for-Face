import boto3
import os
from PIL import Image
import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch

# import logging

# Set up logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

os.environ['TORCH_HOME'] = '/tmp/'


# logger.info("Initializing models...")
mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # initializing mtcnn for face detection
resnet = InceptionResnetV1(pretrained='vggface2').eval() 
# logger.info("Models initialized.")


def handler(event, context):
    # logger.info("Handler started")
    
    s3_client = boto3.client('s3')
    bucket_name = event['bucket_name']
    image_file_name = event['image_file_name']
    data_file_bucket = '1225426618-data'  # Specify the bucket where data.pt is stored
    data_file_key = 'data.pt'  # Specify the key path for data.pt in the bucket

    # Download data.pt from S3
    # logger.info("downloading data.pt")
    s3_client.download_file(data_file_bucket, data_file_key, '/tmp/data.pt')
    # logger.info("data.pt downloaded")
    
    # Proceed with the rest of your function...
    download_path = '/tmp/' + image_file_name
    upload_path = '/tmp/' + image_file_name.split('.')[0] + '.txt'
    
    # Download the image file from S3
    # logger.info(f"Processing file: {image_file_name} from bucket: {bucket_name}")
    s3_client.download_file(bucket_name, image_file_name, download_path)
    # logger.info("Image downloaded")
    
    # Perform face recognition
    result = face_recognition_function(download_path, '/tmp/data.pt')
    
    # Save the result to a file and upload it to S3
    if result:
        with open(upload_path, 'w') as file:
            file.write(result)
        s3_client.upload_file(upload_path, '1225426618-output', os.path.basename(upload_path))

    # logger.info("faceee")
    return {
        'statusCode': 200,
        'body': 'Face recognition completed successfully'
    }

def face_recognition_function(image_path, data_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    face, prob = mtcnn(img_pil, return_prob=True, save_path=None)
    saved_data = torch.load(data_path)
    
    if face is not None:
          # Load data.pt
        emb = resnet(face.unsqueeze(0)).detach()
        embedding_list, name_list = saved_data
        distances = [torch.dist(emb, emb_db).item() for emb_db in embedding_list]
        min_distance = min(distances)
        recognized_name = name_list[distances.index(min_distance)]
        return recognized_name
    else:
        return "No face detected"
