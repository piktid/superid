import os
import sys
import json
import argparse
from time import sleep
from io import BytesIO
from random import randint
from PIL import Image, ImageFile, ImageFilter

from superid_utils import process_single_image
from superid_api import open_image_from_path, open_image_from_url, start_call

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--url', help='Image file url', type=str, default='https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png')
    parser.add_argument('--filepath', help='Input image file absolute path', type=str, default=None)

    parser.add_argument('--upscaler_type', help='Select which upscaler to use: 0 (None), 1 (Soft Portrait), 2 (Hard Portrait), 3 (Mix)', default='3')
    parser.add_argument('--upscaling_mode', help='Select the upscaling mode: fast (takes few seconds, lower quality, currently not available), super (takes up to minutes, higher quality overall)', default='super')
    parser.add_argument('--scale_factor', help='Select the upscaling factor: upscale time 2 or times 4', default='2')
    parser.add_argument('--flag_email', help='Get the upscaled image via email', default=False)
    parser.add_argument('--output_format', help='Save the upscaled image in PNG or JPEG', default='PNG')

    # Parameters only for the normal and super mode
    parser.add_argument('--prompt', help='Describe your image', default=None)
    parser.add_argument('--guidance_scale', help='Guidance scale', type=str, default=None)
    parser.add_argument('--prompt_strength', help='The lower the more similar to the input image, the higher, the more diverse (range 0-1)', type=str, default=None)
    parser.add_argument('--controlnet_scale', help='The higher, the more the upscaling will follow the lines of the input image (range 0-1)', type=str, default=None)
    parser.add_argument('--num_inference_steps', help='The higher, the more denoising steps', default=None)
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

    response = process_single_image(input_image, PARAM_DICTIONARY, TOKEN_DICTIONARY) 
    print(response)  