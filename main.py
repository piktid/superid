import os
import requests
import json
from io import BytesIO
from PIL import Image, ImageFile, ImageFilter
import argparse
from time import sleep
import sys

from superid_api import up_param, start_call, upload_superid_call, upscaling_call, get_notification_call, get_superid_info, get_superid_link

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--upscaler_type', help='Select which upscaler to use: 0 (None), 1 (People), 2 (Scene), 3 (Mix)', default='1')
    parser.add_argument('--upscaling_mode', help='Select the upscaling mode: fast (takes few seconds, lower quality) and normal (takes up to minutes, higher quality)', default='fast')
    parser.add_argument('--scale_factor', help='Select the upscaling factor: upscale time 2 or times 4', default='2')
    parser.add_argument('--output_format', help='Save the upscaled image in PNG or JPEG', default='PNG')
    # Parameters only for the normal mode
    parser.add_argument('--prompt', help='Describe your image', default='')
    parser.add_argument('--prompt_strength', help='The lower the more similar to the input image, the higher, the more diverse (range 0-1)', default='0.1')
    parser.add_argument('--controlnet_scale', help='The higher, the more the upscaling will follow the lines of the input image (range 0-1)', default='0.5')
    parser.add_argument('--num_inference_steps', help='The higher, the more denoising steps', default=20)

    args = parser.parse_args()

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("SUPERID_EMAIL")
    PASSWORD = os.getenv("SUPERID_PASSWORD")

    ## START
    # insert the URL of the image to anonymize
    url = 'https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png' # photo of Lenna
    input_img = Image.open(BytesIO(requests.get(url,stream=False).content))

    # start the call
    TOKEN = start_call(EMAIL, PASSWORD)

    # parameters initialization
    upscaling_parameters = up_param(args)

    # upload
    id_project, id_image = upload_superid_call(input_img, TOKEN)

    # get an estimate of the amount of credits and time needed
    eta, credits, width, height = get_superid_info(id_project, id_image, upscaling_parameters, TOKEN)
    print(f'Image size: {width}, {height}. Estimated time of arrival of upscaled image: {eta}, and estimated credits: {credits}')
    
    # check size condition before proceeding
    if min(width,height)<64:
      print('Minimum size condition is not met, exiting..')
      sys.exit(1)

    # upscale
    output = upscaling_call(id_project, id_image, upscaling_parameters, TOKEN)
    print(f'Upscaling call output: {output}')


    # get the notification, if it is there
    while 1:
      try:
        link = get_superid_link(id_project, id_image, TOKEN)
        print(f'Image available for download at: {link}')
        break
      except:
        # notification is not there yet, wait 10 seconds
        print(f'Server is either booting up or processing your image, waiting {int(eta)} seconds')
      sleep(int(eta))

    # save output_img as you prefer..
    # output_img = Image.open(requests.get(link,stream=True).raw)


