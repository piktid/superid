import os
import sys
import json
from io import BytesIO
from PIL import Image, ImageFile, ImageFilter
from random import randint
from time import sleep

from superid_api import open_image_from_path, open_image_from_url, upload_superid_call, upscaling_call, get_superid_info, get_superid_link

def process_single_image(input_image, PARAM_DICTIONARY, TOKEN_DICTIONARY):

    # UPLOAD
    project_id, image_id = upload_superid_call(input_image, TOKEN_DICTIONARY)

    PARAM_DICTIONARY = {**PARAM_DICTIONARY,'IMAGE_ID': image_id, 'PROJECT_ID': project_id}

    # get an estimate of the amount of credits and time needed
    eta, credits, width, height = get_superid_info(PARAM_DICTIONARY, TOKEN_DICTIONARY)
    print(f'Image size: {width}, {height}. Estimated time of arrival of upscaled image: {eta}, and estimated credits: {credits}')
    
    # check size condition before proceeding
    if min(width,height)<64:
      print('Minimum size condition is not met, exiting..')
      sys.exit(1)

    ## UPSCALE
    output = upscaling_call(PARAM_DICTIONARY, TOKEN_DICTIONARY)
    print(f'Upscaling call output: {output}')


    ## GET THE NOTIFICATION
    i = 0
    while i<10: # max 10 iterations -> then timeout
        i = i+1
        try:
            # check via notifications
            link = get_superid_link(PARAM_DICTIONARY, TOKEN_DICTIONARY)
            print(f'Image available for download at: {link}')
            break
        except:
            # notification is not there yet, wait eta seconds
            print(f'Server is either booting up or processing your image, waiting 30 seconds')
            sleep(30)

    return True