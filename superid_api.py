import json
import base64
import requests
from io import BytesIO
from requests_toolbelt import MultipartEncoder
from PIL import Image, ImageCms


# -----------READ/WRITE FUNCTIONS------------
def open_image_from_url(url):
    response = requests.get(url, stream=True)
    if not response.ok:
        print(response)

    image = Image.open(BytesIO(response.content))
    return image


def open_image_from_path(path):
    f = open(path, 'rb')
    buffer = BytesIO(f.read())
    image = Image.open(buffer)
    return image

    return BytesIO(response.content)


def im_2_B(image):
    # Convert Image to buffer
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    img_str = buff.getvalue()
    return img_str


def im_2_buffer(image):
    # Convert Image to bytes 
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    return buff


def b64_2_img(data):
    # Convert Base64 to Image
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)
    

def im_2_b64(image):
    # Convert Image 
    buff = BytesIO()
    image.save(buff, format='PNG')
    img_str = base64.b64encode(buff.getvalue()).decode('utf-8')
    return img_str


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
def upload_superid_call(src_img, TOKEN_DICTIONARY):
    # Upload the image into PiktID's servers and get the id of the project and of the image
    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    src_img_B = im_2_buffer(src_img)

    options = '0'
    m = MultipartEncoder(
                        fields={'options': options,
                                'file': ('file', src_img_B, 'text/plain')}
                        )
    
    response = requests.post(URL_API+'/upload_extra', 
                             headers={
                                      "Content-Type": m.content_type,
                                      'Authorization': 'Bearer '+TOKEN},
                             data=m,
                             )

    response_json = json.loads(response.text)
    # print(response_json)
    
    id_project = response_json.get('id_project')
    id_image = response_json.get('id_image')

    return id_project, id_image


def update_data_upscaling_call(data, PARAM_DICTIONARY):
    # update the json data first

    GUIDANCE_SCALE = PARAM_DICTIONARY.get('GUIDANCE_SCALE')
    PROMPT_STRENGTH = PARAM_DICTIONARY.get('PROMPT_STRENGTH')
    CONTROLNET_SCALE = PARAM_DICTIONARY.get('CONTROLNET_SCALE')

    if GUIDANCE_SCALE is not None:
        data.update({'guidance_scale': GUIDANCE_SCALE})
        
    if PROMPT_STRENGTH is not None:
        data.update({'prompt_strength': PROMPT_STRENGTH})

    if CONTROLNET_SCALE is not None:
        data.update({'controlnet_conditioning_scale': CONTROLNET_SCALE})

    # extra options

    FACE_FIXER = PARAM_DICTIONARY.get('FACE_FIXER')
    DENOISE_INPUT = PARAM_DICTIONARY.get('DENOISE_INPUT')

    OPTIONS_DICT = {}

    if FACE_FIXER is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'face_enhancer': FACE_FIXER}

    if DENOISE_INPUT is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'denoise_input': DENOISE_INPUT}

    OPTIONS = json.dumps(OPTIONS_DICT)
    extra_options = {'options': OPTIONS}
    data.update(extra_options)

    return data


def upscaling_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    id_project = PARAM_DICTIONARY.get('PROJECT_ID') 
    id_image = PARAM_DICTIONARY.get('IMAGE_ID') 
    seed = PARAM_DICTIONARY.get('SEED')
    scale_factor = PARAM_DICTIONARY.get('SCALE_FACTOR')
    upscaler_type = PARAM_DICTIONARY.get('UPSCALER_TYPE', '4')
    upscaling_mode = PARAM_DICTIONARY.get('UPSCALING_MODE', 'super')
    flag_email = PARAM_DICTIONARY.get('FLAG_EMAIL')
    output_format = PARAM_DICTIONARY.get('OUTPUT_FORMAT')

    data = {'id_project': id_project, 
            'id_image': id_image, 
            'scale_factor': scale_factor, 
            'upscaler_type': upscaler_type, 
            'upscaling_mode': upscaling_mode, 
            'flag_email': flag_email, 
            'output_format': output_format, 
            'seed': seed
            }

    data = update_data_upscaling_call(data, PARAM_DICTIONARY)
    print(f'data to send to upscale: {data}')

    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/superid', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             json=data,
                             )

    response_json = json.loads(response.text)

    return response_json


def upscaling_fast_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):
    id_project = PARAM_DICTIONARY.get('PROJECT_ID') 
    id_image = PARAM_DICTIONARY.get('IMAGE_ID') 
    seed = PARAM_DICTIONARY.get('SEED')
    scale_factor = PARAM_DICTIONARY.get('SCALE_FACTOR')
    flag_email = PARAM_DICTIONARY.get('FLAG_EMAIL')
    output_format = PARAM_DICTIONARY.get('OUTPUT_FORMAT')

    data = {'id_project': id_project, 
            'id_image': id_image, 
            'scale_factor': scale_factor, 
            'flag_email': flag_email, 
            'output_format': output_format, 
            'seed': seed
            }

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

    upscaling_mode = PARAM_DICTIONARY.get('UPSCALING_MODE', 'super')
    strength = PARAM_DICTIONARY.get('PROMPT_STRENGTH', '0.35')

    data = {'id_project': id_project, 'id_image': id_image, 'scale_factor': scale_factor, 'upscaling_mode': upscaling_mode, 
            'strength': strength, 'num_inference_steps': 20}

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