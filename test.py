import asyncio
from email.mime import image
import io
import glob
import os
import sys
import time
from urllib import response
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition

# This key will serve all examples in this document.
KEY = "bc8561e0a6cb4ff9b0d7015c45f91ee7"
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://ia-compsci-23.cognitiveservices.azure.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# PUT IN ANY IMAGE YOU WANT!!!!! IT WORKS
image_url = 'https://www.business2community.com/wp-content/uploads/2015/10/42454567_m.jpg.jpg'

def Detection(img_url):
    image_name = os.path.basename(img_url)

    response_detected_faces = face_client.face.detect_with_url(
        image_url, 
        detection_model='detection_03',
        recognition_model='recognition_04',
    )
    print(response_detected_faces)

    if not response_detected_faces:
        raise Exception('No face detected')

    print('Number of people detected: {0}' .format(len(response_detected_faces)))

    person1 = response_detected_faces[0]
    # print(vars(person1))
    # print(person1.face_rectangle)

    response_image = requests.get(image_url)
    img = Image.open(io.BytesIO(response_image.content))
    draw = ImageDraw.Draw(img)

    for face in response_detected_faces:
        rect = face.face_rectangle
        left = rect.left
        top = rect.top
        right = rect.width + left
        bottom = rect.height + top
        draw.rectangle(((left,top),(right,bottom)), outline='blue', width = 5)

    img.show()

def Comparison():

    response_detected_faces = face_client.face.detect_with_stream(
        image=open('test_images/Group#1.jpeg','rb'),
        detection_model='detection_03',
        recognition_model='recognition_04',
        return_face_landmarks=True
    )

# faces to check against
    face_ids = [ face.face_id for face in response_detected_faces]
    
    img_target = open('test_images/Noah#1.jpeg', 'rb')
    response_face_target = face_client.face.detect_with_stream(
        image = img_target,
        detection_model='detection_03',
        recognition_model='recognition_04'
    )
    target_face_id = response_face_target[0].face_id

    matched_face_ids = face_client.face.find_similar(
        face_id=target_face_id,
        face_ids=face_ids
    )

    print(matched_face_ids)



def main():
    Comparison() 

if __name__ == "__main__":
    main()
