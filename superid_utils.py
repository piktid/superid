import sys
from time import sleep

from superid_api import upload_superid_call, upscaling_call, upscaling_fast_call, get_superid_info, get_superid_link


def process_single_image(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    # UPLOAD
    project_id, image_id = upload_superid_call(PARAM_DICTIONARY, TOKEN_DICTIONARY)

    PARAM_DICTIONARY = {**PARAM_DICTIONARY, 'IMAGE_ID': image_id, 'PROJECT_ID': project_id}

    # get an estimate of the amount of credits and time needed
    eta, credits, width, height = get_superid_info(PARAM_DICTIONARY, TOKEN_DICTIONARY)
    print(f'Image size: {width}, {height}. Estimated time of arrival of upscaled image: {eta}, and estimated credits: {credits}')
    scale_factor = int(PARAM_DICTIONARY.get('SCALE_FACTOR'))
    width_o, height_o = scale_factor*width, scale_factor*height
    # check size condition before proceeding
    if min(width, height) < 64 or max(width_o, height_o) > 8192:
        print('Minimum/maximum size condition is not met, exiting..')
        sys.exit(1)

    # UPSCALE
    if PARAM_DICTIONARY.get('FAST', False):
        output = upscaling_fast_call(PARAM_DICTIONARY, TOKEN_DICTIONARY)
        print(f'Upscaling call output: {output}')
    else:
        output = upscaling_call(PARAM_DICTIONARY, TOKEN_DICTIONARY)
        print(f'Upscaling call output: {output}')

    # GET THE NOTIFICATION
    i = 0
    while i < 100:  # max 100 iterations -> then timeout
        i = i+1
        # check via notifications
        link = get_superid_link(PARAM_DICTIONARY, TOKEN_DICTIONARY)
        if link is not None:
            print(f'Image available for download at: {link}')
            break
    
        # notification is not there yet, wait eta seconds
        print('Server is either booting up or processing your image, waiting 10 seconds')
        sleep(10)

    return True