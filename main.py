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

    parser.add_argument('--scale_factor', help='Select the upscaling factor: upscale times 1, 2 or 4', default='2')
    parser.add_argument('--email', help='Get the upscaled image via email', action='store_true')
    parser.add_argument('--output_format', help='Save the upscaled image in PNG or JPEG', default='PNG')

    # Parameters only for the superid mode
    parser.add_argument('--prompt', help='Describe your image', default='')
    parser.add_argument('--fractality', help='Fractality, the higher the more adherent to the prompt (range 1-20)', type=int, default=3)
    parser.add_argument('--creativity', help='Creativity, the lower the more similar to the input image, the higher, the more diverse (range 1-20)', type=int, default=7)
    parser.add_argument('--fidelity', help='Fidelity, the higher, the more the upscaling will follow the resemblance of the input image (range 0-20)', type=int, default=5)
    parser.add_argument('--denoise', help='Denoise filter amount (range 0-20)', type=int, default=1)    
    parser.add_argument('--seed', help='Upscaling seed', type=int, default=randint(0, 100000))
    parser.add_argument('--face_enhancer', help='Enhance small faces', action='store_true')

    # Parameters for the fast mode
    parser.add_argument('--fast', help='Fast mode', action='store_true')
    parser.add_argument('--force_face_enhancer', help='Force face enhancer on all faces', action='store_true')

    # Parameters for image enhancement
    parser.add_argument('--no_image_filters', help='Do not apply set of filters', action='store_false')
    parser.add_argument('--no_match_colors', help='Do not match colors', action='store_false')

    args = parser.parse_args()

    # Validation checks
    if args.output_format.upper() not in ['PNG', 'JPEG']:
        print(f"Error: Invalid output format '{args.output_format}'. Must be 'PNG' or 'JPEG'.")
        sys.exit(1)
    
    if args.scale_factor not in ['1', '2', '4']:
        print(f"Error: Invalid scale factor '{args.scale_factor}'. Must be '1', '2' or '4'.")
        sys.exit(1)

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("SUPERID_EMAIL")
    PASSWORD = os.getenv("SUPERID_PASSWORD")

    # Upscaling parameters
    FAST_FLAG = args.fast
    SCALE_FACTOR = args.scale_factor
    FLAG_EMAIL = args.email
    OUTPUT_FORMAT = args.output_format.upper()  # Normalize to uppercase

    # Superid parameters
    PROMPT = args.prompt
    FRACTALITY = args.fractality
    CREATIVITY = args.creativity
    FIDELITY = args.fidelity
    SEED = args.seed
    FACE_ENHANCER = args.face_enhancer
    DENOISE = args.denoise

    # Fast parameters
    FORCE_FACE_ENHANCER = args.force_face_enhancer

    # Image enhancement parameters
    IMAGE_FILTERS_FLAG = args.no_image_filters
    MATCH_COLORS_FLAG = args.no_match_colors

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
            'FORCE_FACE_ENHANCER': FORCE_FACE_ENHANCER,
            'IMAGE_FILTERS_FLAG': IMAGE_FILTERS_FLAG,
            'MATCH_COLORS_FLAG': MATCH_COLORS_FLAG,
        }

    response = process_single_image(PARAM_DICTIONARY, TOKEN_DICTIONARY) 
    print(response)