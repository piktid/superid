import os
import sys
import json
import argparse
from time import sleep
from io import BytesIO
from random import randint
from PIL import Image, ImageFile, ImageFilter

from superid_api import open_image_from_path, open_image_from_url, start_call, upload_superid_call, upscaling_call, get_superid_info, get_superid_link

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--url', help='Image file url', type=str, default='http://www.lenna.org/len_std.jpg')
    parser.add_argument('--filepath', help='Input image file absolute path', type=str, default=None)

    parser.add_argument('--upscaler_type', help='Select which upscaler to use: 0 (None), 1 (People), 2 (Scene), 3 (Mix)', default='1')
    parser.add_argument('--upscaling_mode', help='Select the upscaling mode: fast (takes few seconds, lower quality), normal (takes up to minutes, higher quality on faces), super (takes up to minutes/hours, higher quality overall)', default='fast')
    parser.add_argument('--scale_factor', help='Select the upscaling factor: upscale time 2 or times 4', default='2')
    parser.add_argument('--flag_email', help='Get the upscaled image via email', default=False)
    parser.add_argument('--output_format', help='Save the upscaled image in PNG or JPEG', default='PNG')

    # Parameters only for the normal and super mode
    parser.add_argument('--prompt', help='Describe your image', default='')
    parser.add_argument('--guidance_scale', help='Guidance scale', type=str, default=None)
    parser.add_argument('--prompt_strength', help='The lower the more similar to the input image, the higher, the more diverse (range 0-1)', type=str, default=None)
    parser.add_argument('--controlnet_scale', help='The higher, the more the upscaling will follow the lines of the input image (range 0-1)', type=str, default=None)
    parser.add_argument('--num_inference_steps', help='The higher, the more denoising steps', default=20)
    parser.add_argument('--seed', help='Upscaling seed', type=int, default=randint(0,100000))


    args = parser.parse_args()

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("SUPERID_EMAIL")
    PASSWORD = os.getenv("SUPERID_PASSWORD")

    # Upscaling parameters
    UPSCALER_TYPE = args.upscaler_type
    UPSCALING_MODE = args.upscaling_mode
    SCALE_FACTOR = args.scale_factor
    FLAG_EMAIL = args.flag_email
    OUTPUT_FORMAT = args.output_format

    PROMPT = args.prompt
    GUIDANCE_SCALE = args.guidance_scale
    PROMPT_STRENGTH = args.prompt_strength
    CONTROLNET_SCALE = args.controlnet_scale
    STEPS = args.num_inference_steps
    SEED = args.seed

    # Image parameters
    URL = args.url 
    INPUT_PATH = args.filepath

    if INPUT_PATH is not None:
        if os.path.exists(INPUT_PATH):
            input_image = open_image_from_path(INPUT_PATH)
            print(f'Using as input image the file located at: {INPUT_PATH}')
        else:
            print('Wrong filepath, check again')
            sys.exit()
    else:
        try:
            input_image = open_image_from_url(URL)
            print(f'Using as input image the file located at: {URL}')
        except:
            print('Wrong URL, check again')
            sys.exit()


    # log in
    TOKEN_DICTIONARY = start_call(EMAIL, PASSWORD)


    UPSCALER_TYPE = args.upscaler_type
    UPSCALING_MODE = args.upscaling_mode
    SCALE_FACTOR = args.scale_factor
    FLAG_EMAIL = args.flag_email
    OUTPUT_FORMAT = args.output_format

    PROMPT = args.prompt
    GUIDANCE_SCALE = args.guidance_scale
    PROMPT_STRENGTH = args.prompt_strength
    CONTROLNET_SCALE = args.controlnet_scale
    STEPS = args.num_inference_steps
    SEED = args.seed


    PARAM_DICTIONARY = {
            'INPUT_PATH':INPUT_PATH,
            'UPSCALER_TYPE': UPSCALER_TYPE,
            'UPSCALING_MODE':UPSCALING_MODE,
            'SCALE_FACTOR':SCALE_FACTOR,
            'FLAG_EMAIL':FLAG_EMAIL,
            'OUTPUT_FORMAT':OUTPUT_FORMAT,
            'SEED':SEED,
            'PROMPT':PROMPT,
            'GUIDANCE_SCALE': GUIDANCE_SCALE,
            'PROMPT_STRENGTH': PROMPT_STRENGTH,
            'CONTROLNET_SCALE': CONTROLNET_SCALE,
            'STEPS': STEPS,
        }

    ## UPLOAD
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
    while 1:
      try:
        link = get_superid_link(PARAM_DICTIONARY, TOKEN_DICTIONARY)
        print(f'Image available for download at: {link}')
        break
      except:
        # notification is not there yet, wait eta seconds
        print(f'Server is either booting up or processing your image, waiting 30 seconds')
      sleep(30)

