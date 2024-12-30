import os
import sys
import argparse
from random import randint

from superid_utils import process_single_image
from superid_api import open_image_from_path, open_image_from_url, start_call

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--url', help='Image file url', type=str, default='https://images.piktid.com/frontend/studio/superid/upscaler_sample/21z.png')
    parser.add_argument('--filepath', help='Input image file absolute path', type=str, default=None)

    parser.add_argument('--fast', help='Use the fast upscaler', action='store_true')
    parser.add_argument('--scale_factor', help='Select the upscaling factor: upscale time 2 or times 4', default='2')
    parser.add_argument('--email', help='Get the upscaled image via email', action='store_true')
    parser.add_argument('--output_format', help='Save the upscaled image in PNG or JPEG', default='PNG')

    # Parameters only for the normal and super mode
    parser.add_argument('--prompt', help='Describe your image', default='')
    parser.add_argument('--guidance_scale', help='Guidance scale', type=str, default='3')
    parser.add_argument('--prompt_strength', help='Creativity, the lower the more similar to the input image, the higher, the more diverse (range 0-1)', type=str, default='0.35')
    parser.add_argument('--controlnet_scale', help='Fidelity, the higher, the more the upscaling will follow the resemblance of the input image (range 0-1)', type=str, default='0.5')
    parser.add_argument('--seed', help='Upscaling seed', type=int, default=randint(0, 100000))

    # Pre-post processing parameters
    parser.add_argument('--face_fixer', help='Fix small faces', action='store_true')
    parser.add_argument('--denoise_input', help='Denoise filter amount, range 0-1', type=str, default='0.0')

    args = parser.parse_args()

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("SUPERID_EMAIL")
    PASSWORD = os.getenv("SUPERID_PASSWORD")

    # Upscaling parameters
    FAST_FLAG = args.fast
    SCALE_FACTOR = args.scale_factor
    FLAG_EMAIL = args.email
    OUTPUT_FORMAT = args.output_format

    PROMPT = args.prompt
    GUIDANCE_SCALE = args.guidance_scale
    PROMPT_STRENGTH = args.prompt_strength
    CONTROLNET_SCALE = args.controlnet_scale
    SEED = args.seed

    FACE_FIXER = args.face_fixer
    DENOISE_INPUT = args.denoise_input

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
            'INPUT_PATH': INPUT_PATH,
            'SCALE_FACTOR': SCALE_FACTOR,
            'FLAG_EMAIL': FLAG_EMAIL,
            'OUTPUT_FORMAT': OUTPUT_FORMAT,
            'SEED': SEED,
            'PROMPT': PROMPT,
            'GUIDANCE_SCALE': GUIDANCE_SCALE,
            'PROMPT_STRENGTH': PROMPT_STRENGTH,
            'CONTROLNET_SCALE': CONTROLNET_SCALE,
            'FACE_FIXER': FACE_FIXER,
            'DENOISE_INPUT': DENOISE_INPUT,
            'FAST': FAST_FLAG,
        }

    response = process_single_image(input_image, PARAM_DICTIONARY, TOKEN_DICTIONARY) 
    print(response)