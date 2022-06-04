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
# ZIP file management
from zipfile import ZipFile

# IMAGE FILE EXTENSIONS
img_extensions = ['.jpg','.jpeg','.png','.heif']

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

# Based on EXAMPLE #1
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

def RetriveImages():
    print('got da images')

# Who do we want to find
target_person = 'test_images/Noah#1.jpeg'
# What images do we want to check
imgs_to_check = []

# Taking out all of the image files
def extract_Compare(zip_address):
    file_name, file_extension = os.path.splitext(zip_address)
    if(file_extension == '.zip'):
        # VALID ZIP FILE
        with ZipFile(zip_address, 'r') as zip:
            # printing all the contents of the zip file
            # file.printdir()
            zip_files = zip.namelist() # list of all the file names :D
            imgs = [] #empty list to store VALID files we want to extract
            for file in zip_files:
                file_name, file_extension = os.path.splitext(file)
                if(file_extension in img_extensions):
                    imgs.append(file)
                    zip.extract(file,path='store') # We store all the images in a temporary space called store
            print(imgs)
            
    else:
        print("That Ain't a ZIP buddy")

# File management at it's finest
def clear_dir(dir_path):
    files = os.listdir(dir_path)
    for file in files:
        try:
            # remove the files
            os.remove(dir_path+'/'+file)
        except:
            # here it isn't a file so it can only be a dir
            os.rmdir(dir_path+'/'+file)
    print(dir_path + 'was cleared')

# Based on EXAMPLE #4
def Comparison(target_img, compare_img):

    # This is the image that we want to check
    compared_to = compare_img
    response_detected_faces = face_client.face.detect_with_stream(
        image=open(compared_to,'rb'),
        detection_model='detection_03',
        recognition_model='recognition_04'
    )

    # faces to check against
    face_ids = [ face.face_id for face in response_detected_faces]
        
    # This would be the image of the student we want to find
    # a clean image with just them is what we need to be inputed
    img_target = open(target_img, 'rb')
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

# WHERE TO RUN ANY METHODS YOU MAKE :DDD What's in here is what runs
def main():
    # Getting all files
    extract_Compare('test_images/Group.zip')
    extract_Compare('test_images/Wrong.zip')
    #now they are in store

    # TO DO: Get them out of store and run 

    # for img in imgs_to_check:
    #   Comparison(target_person, img)
   
    clear_dir('store')
    print('MAIN COMPLETE :D')

if __name__ == "__main__":
    main()
