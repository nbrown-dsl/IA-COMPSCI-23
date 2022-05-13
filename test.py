import asyncio
from email.mime import image
import io
import glob
import os
import sys
import time
from turtle import color
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

# Abstracting my KEY and ENDPOINT away from this file :D
# They are stored in a .gitignore file with the information on seperate lines
APIstuff = 'API.txt'
def setup_API(filepath):
    f = open(filepath, "r")
    read = f.read().splitlines()
    return read

credz = setup_API(APIstuff)
# This key will serve all examples in this document.
KEY = credz[0]
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = credz[1]

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

""" Based on Example #4"""
def Comparison():

    compared_to = 'test_images/Charles+Anastasia.jpeg'
    response_detected_faces = face_client.face.detect_with_stream(
        image=open(compared_to,'rb'),
        detection_model='detection_03',
        recognition_model='recognition_04'
    )

    # faces to check against
    face_ids = [ face.face_id for face in response_detected_faces]
        
    # This would be the image of the student we want to find
    # a clean image with just them is what we need to be inputed
    img_target = open('test_images/Noah#1.jpeg', 'rb')
    response_face_target = face_client.face.detect_with_stream(
        image = img_target,
        detection_model='detection_03',
        recognition_model='recognition_04'
    )
    target_face_id = response_face_target[0].face_id

    # Now we have both our target face id,
    # And we compare it against all the face ids from face_ids
    matched_face_ids = face_client.face.find_similar(
        face_id=target_face_id,
        face_ids=face_ids
    )

    # Open the group image / one you want to check if the student is in
    img = Image.open(open(compared_to, 'rb'))
    draw = ImageDraw.Draw(img)

    #Flag raising for if we find a match
    matched = False

    # draw a box around all matches of the face
    for matched_face in matched_face_ids:
        for face in response_detected_faces:
            if face.face_id == matched_face.face_id:
                rect = face.face_rectangle
                left = rect.left
                top = rect.top
                right = rect.width + left
                bottom = rect.height + top
                draw.rectangle(((left, top), (right, bottom)), outline='green', width=5)
                matched = True
    
    if matched == False:
        draw.line([(0,0),(img.size[0],img.size[1])],fill='red', width=5)

    img.show()



def main():
    Comparison() 
    print('main')

if __name__ == "__main__":
    main()
