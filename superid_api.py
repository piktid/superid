import json
import requests
from io import BytesIO

# ---QUICK UTILS---
def extract_link(data_list, id_image, id_project):
    for item in data_list:
        if item['data']['id_image'] == id_image and item['data']['id_project'] == id_project:
            return item['data']['link']['l']
    return None


# -----------PROCESSING FUNCTIONS------------
def start_call(email, password):
    # Get token
    URL_API = 'https://api.piktid.com/api'
    print(f'Logging to: {URL_API}')

    response = requests.post(URL_API+'/tokens', data={}, auth=(email, password))
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']

    return {'access_token': ACCESS_TOKEN, 'refresh_token': REFRESH_TOKEN, 'url_api': URL_API}


def refresh_call(TOKEN_DICTIONARY):
    # Get token using only access and refresh tokens, no mail and psw
    URL_API = TOKEN_DICTIONARY.get('url_api')
    response = requests.put(URL_API+'/tokens', json=TOKEN_DICTIONARY)
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']

    return {'access_token': ACCESS_TOKEN, 'refresh_token': REFRESH_TOKEN, 'url_api': URL_API}


# UPLOAD
def upload_superid_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    # Upload the image into PiktID's servers and get the id of the project and of the image
    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    target_full_path = PARAM_DICTIONARY.get('INPUT_PATH')
    if target_full_path is None:
        target_url = PARAM_DICTIONARY.get('INPUT_URL')
        image_response = requests.get(target_url)
        image_response.raise_for_status()  
        image_file = BytesIO(image_response.content)
        image_file.name = 'target.jpg' 
        
    else:
        image_file = open(target_full_path, 'rb')

    # request with file
    response = requests.post(URL_API+'/superid/upload', 
                                headers={'Authorization': 'Bearer '+TOKEN},
                                files={'file': image_file},
                                )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token', '')
        # try with new TOKEN
        response = requests.post(URL_API+'/superid/upload', 
                                    headers={'Authorization': 'Bearer '+TOKEN},
                                    files={'file': image_file},
                                    )

    response_json = json.loads(response.text)
    print(f"Upload successful. Response json: {response_json}")

    id_project = response_json.get('id_project')
    id_image = response_json.get('id_image')

    return id_project, id_image


def update_data_upscaling_call(data, PARAM_DICTIONARY):
    # update the json data first

    FRACTALITY = PARAM_DICTIONARY.get('FRACTALITY')
    CREATIVITY = PARAM_DICTIONARY.get('CREATIVITY')
    FIDELITY = PARAM_DICTIONARY.get('FIDELITY')
    SEED = PARAM_DICTIONARY.get('SEED')
    DENOISE = PARAM_DICTIONARY.get('DENOISE')
    FACE_ENHANCER = PARAM_DICTIONARY.get('FACE_ENHANCER')
    PROMPT = PARAM_DICTIONARY.get('PROMPT')

    FORCE_FACE_ENHANCER = PARAM_DICTIONARY.get('FORCE_FACE_ENHANCER')
    IMAGE_FILTERS_FLAG = PARAM_DICTIONARY.get('IMAGE_FILTERS_FLAG')
    MATCH_COLORS_FLAG = PARAM_DICTIONARY.get('MATCH_COLORS_FLAG')

    OPTIONS_DICT = {}

    # Superid parameters
    if FRACTALITY is not None:
        data.update({'fractality': FRACTALITY})
        
    if CREATIVITY is not None:
        data.update({'creativity': CREATIVITY})

    if FIDELITY is not None:
        data.update({'fidelity': FIDELITY})

    if DENOISE is not None:
        data.update({'denoise': DENOISE})

    if FACE_ENHANCER is not None:
        data.update({'face_enhancer': FACE_ENHANCER})

    if SEED is not None:
        data.update({'seed': SEED})

    if PROMPT is not None:
        data.update({'prompt': PROMPT})

    # Options parameters
    if FORCE_FACE_ENHANCER is not None:
        OPTIONS_DICT.update({'force_fixer': FORCE_FACE_ENHANCER})

    # Image enhancement parameters
    if IMAGE_FILTERS_FLAG is not None:
        OPTIONS_DICT.update({'image_filters_flag': IMAGE_FILTERS_FLAG})

    if MATCH_COLORS_FLAG is not None:
        OPTIONS_DICT.update({'match_colors_flag': MATCH_COLORS_FLAG})

    OPTIONS = json.dumps(OPTIONS_DICT)
    extra_options = {'options': OPTIONS}
    data.update(extra_options)

    # contact us for more parameters
    return data


def upscaling_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    id_project = PARAM_DICTIONARY.get('PROJECT_ID') 
    id_image = PARAM_DICTIONARY.get('IMAGE_ID') 
    scale_factor = PARAM_DICTIONARY.get('SCALE_FACTOR')
    flag_email = PARAM_DICTIONARY.get('FLAG_EMAIL')
    output_format = PARAM_DICTIONARY.get('OUTPUT_FORMAT')

    data = {'id_project': id_project, 
            'id_image': id_image, 
            'scale_factor': scale_factor, 
            'flag_email': flag_email, 
            'output_format': output_format
            }

    data = update_data_upscaling_call(data, PARAM_DICTIONARY)
    print(f'data to send to upscale: {data}')

    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/superid/v2', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             json=data,
                             )
    
    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token', '')
        # try with new TOKEN
        response = requests.post(URL_API+'/superid/v2', 
                                 headers={'Authorization': 'Bearer '+TOKEN},
                                 json=data,
                                 )

    response_json = json.loads(response.text)

    return response_json


def update_data_upscaling_fast_call(data, PARAM_DICTIONARY):
    # update the json data first

    SEED = PARAM_DICTIONARY.get('SEED')
    FORCE_FACE_ENHANCER = PARAM_DICTIONARY.get('FORCE_FACE_ENHANCER')
    IMAGE_FILTERS_FLAG = PARAM_DICTIONARY.get('IMAGE_FILTERS_FLAG')
    MATCH_COLORS_FLAG = PARAM_DICTIONARY.get('MATCH_COLORS_FLAG')

    OPTIONS_DICT = {}

    if SEED is not None:
        data.update({'seed': SEED})

    # Options parameters
    if FORCE_FACE_ENHANCER is not None:
        OPTIONS_DICT.update({'force_fixer': FORCE_FACE_ENHANCER})

    # Image enhancement parameters
    if IMAGE_FILTERS_FLAG is not None:
        OPTIONS_DICT.update({'image_filters_flag': IMAGE_FILTERS_FLAG})

    if MATCH_COLORS_FLAG is not None:
        OPTIONS_DICT.update({'match_colors_flag': MATCH_COLORS_FLAG})

    OPTIONS = json.dumps(OPTIONS_DICT)
    extra_options = {'options': OPTIONS}
    data.update(extra_options)

    return data


def upscaling_fast_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    id_project = PARAM_DICTIONARY.get('PROJECT_ID') 
    id_image = PARAM_DICTIONARY.get('IMAGE_ID') 
    scale_factor = PARAM_DICTIONARY.get('SCALE_FACTOR')
    flag_email = PARAM_DICTIONARY.get('FLAG_EMAIL')
    output_format = PARAM_DICTIONARY.get('OUTPUT_FORMAT')

    data = {'id_project': id_project, 
            'id_image': id_image, 
            'scale_factor': scale_factor, 
            'flag_email': flag_email, 
            'output_format': output_format 
            }

    data = update_data_upscaling_fast_call(data, PARAM_DICTIONARY)
    print(f'data to send to fast upscale: {data}')

    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/superid_fast', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             json=data,
                             )

    # print(response.content)
    response_json = json.loads(response.text)

    return response_json


# NOTIFICATION FUNCTIONS
def get_notification_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/notification_by_name_json', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             json={'name_list': 'superid'}
                             )
    response_json = json.loads(response.text)
    return response_json.get('notifications_list')


def get_superid_info(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    # get ETA and credits needed for upscaling
    id_project = PARAM_DICTIONARY.get('PROJECT_ID') 
    id_image = PARAM_DICTIONARY.get('IMAGE_ID') 
    scale_factor = PARAM_DICTIONARY.get('SCALE_FACTOR')

    data = {'id_project': id_project, 'id_image': id_image, 'scale_factor': scale_factor, 'upscaling_mode': 'normal', 
            'strength': '0.35', 'num_inference_steps': 20}

    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.get(URL_API+'/superid_info', 
                            headers={'Authorization': 'Bearer '+TOKEN},
                            json=data,
                            )
    
    response_json = json.loads(response.text)
    eta = response_json.get('eta')
    credits = response_json.get('required_credits')
    width = response_json.get('width')
    height = response_json.get('height')

    return eta, credits, width, height


def get_superid_link(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    # get info on the upscaled image
    id_project = PARAM_DICTIONARY.get('PROJECT_ID') 
    id_image = PARAM_DICTIONARY.get('IMAGE_ID') 

    # extract notifications
    notifications_list = get_notification_call(PARAM_DICTIONARY, TOKEN_DICTIONARY)

    link = extract_link(notifications_list, id_image, id_project)
    
    return link