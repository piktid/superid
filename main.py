import os
import sys
import argparse
from random import randint

from superid_utils import process_single_image
from superid_api import start_call

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
    parser.add_argument('--fractality', help='Fractality, the higher the more adherent to the prompt (range 1-20)', type=int, default=3)
    parser.add_argument('--creativity', help='Creativity, the lower the more similar to the input image, the higher, the more diverse (range 1-20)', type=int, default=7)
    parser.add_argument('--fidelity', help='Fidelity, the higher, the more the upscaling will follow the resemblance of the input image (range 0-20)', type=int, default=5)
    parser.add_argument('--denoise', help='Denoise filter amount (range 0-20)', type=int, default=1)    
    parser.add_argument('--seed', help='Upscaling seed', type=int, default=randint(0, 100000))
    parser.add_argument('--face_enhancer', help='Enhance small faces', action='store_true')

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
    FRACTALITY = args.fractality
    CREATIVITY = args.creativity
    FIDELITY = args.fidelity
    SEED = args.seed
    FACE_ENHANCER = args.face_enhancer
    DENOISE = args.denoise

    # Image parameters
    INPUT_URL = args.url 
    INPUT_PATH = args.filepath

    if INPUT_PATH is not None:
        if os.path.exists(INPUT_PATH):
            print(f'Using as input image the file located at: {INPUT_PATH}')
        else:
            print('Wrong filepath, check again')
            sys.exit()
    else:
        if INPUT_URL is not None:
            print(f'Using as input image the file located at: {INPUT_URL}')
        else:
            print('Wrong URL, check again')
            sys.exit()

    # log in
    TOKEN_DICTIONARY = start_call(EMAIL, PASSWORD)

    PARAM_DICTIONARY = {
            'INPUT_PATH': INPUT_PATH,
            'INPUT_URL': INPUT_URL,
            'SCALE_FACTOR': SCALE_FACTOR,
            'FLAG_EMAIL': FLAG_EMAIL,
            'OUTPUT_FORMAT': OUTPUT_FORMAT,
            'SEED': SEED,
            'PROMPT': PROMPT,
            'FRACTALITY': FRACTALITY,
            'CREATIVITY': CREATIVITY,
            'FIDELITY': FIDELITY,
            'DENOISE': DENOISE,
            'FACE_ENHANCER': FACE_ENHANCER,
            'FAST': FAST_FLAG,
        }

    response = process_single_image(PARAM_DICTIONARY, TOKEN_DICTIONARY) 
    print(response)