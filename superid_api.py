import os
import requests
import json
from io import BytesIO
import base64
from PIL import Image, ImageFile, ImageFilter, ImageCms
import copy
import time
from requests_toolbelt import MultipartEncoder


URL_API = 'https://api.piktid.com/api'

##----UPSCALING CLASS----
# Do not modify the parameters unless you are an expert
class up_param():
    def __init__(self, args):
        self.upscaler_type = args.upscaler_type
        self.upscaling_mode = args.upscaling_mode
        self.scale_factor = args.scale_factor
        self.output_format = args.output_format
        self.prompt = args.prompt
        self.controlnet_scale = args.controlnet_scale
        self.prompt_strength = args.prompt_strength
        self.num_inference_steps = args.num_inference_steps

## -----------READ/WRITE FUNCTIONS------------
def open_image_from_url(url):
    response = requests.get(url, stream=True)
    if not response.ok:
        print(response)

    image = Image.open(BytesIO(response.content))
    return image

def open_image_from_url_bytes(url, only_face=False):
    response = requests.get(url, stream=True)
    if not response.ok:
        print(response)

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


## -----------PROCESSING FUNCTIONS------------
def start_call(email, password):
    # Get token
    response = requests.post(URL_API+'/tokens', data={}, auth=(email, password))
    response_json = json.loads(response.text)
    TOKEN = response_json['access_token']

    return TOKEN

def upload_superid_call(src_img, TOKEN):
    # Upload the image into PiktID's servers and get the id of the project and of the image
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
    print(response_json)
    
    id_project = response_json.get('id_project')
    id_image = response_json.get('id_image')

    return id_project, id_image

def upscaling_call(id_project, id_image, upscaling_parameters, TOKEN):

    scale_factor = upscaling_parameters.scale_factor
    upscaler_type = upscaling_parameters.upscaler_type
    upscaling_mode = upscaling_parameters.upscaling_mode
    output_format = upscaling_parameters.output_format
    prompt = upscaling_parameters.prompt
    controlnet_scale = upscaling_parameters.controlnet_scale
    prompt_strength = upscaling_parameters.prompt_strength
    num_inference_steps = upscaling_parameters.num_inference_steps

    response = requests.post(URL_API+'/superid', 
        headers={'Authorization': 'Bearer '+TOKEN},
        json={'id_project':id_project, 'id_image':id_image, 'prompt': prompt, 'scale_factor':scale_factor, 'upscaler_type':upscaler_type, 'upscaling_mode':upscaling_mode, 'prompt_strength':prompt_strength, 'controlnet_conditioning_scale': controlnet_scale, 'num_inference_steps':num_inference_steps, 'output_format':output_format},
        )

    print(response.content)
    response_json = json.loads(response.text)

    return response_json

# NOTIFICATION FUNCTIONS
def get_notification_call(TOKEN):

    response = requests.post(URL_API+'/notification_by_name', 
        headers={'Authorization': 'Bearer '+TOKEN},
        json={'name_list':'superid'}
        )
    print(f'response: {response.text}')
    return

def get_superid_info(id_project, id_image, upscaling_parameters, TOKEN):
    # get ETA and credits needed for generation
    scale_factor = upscaling_parameters.scale_factor
    upscaling_mode = upscaling_parameters.upscaling_mode
    strength = upscaling_parameters.prompt_strength
    num_inference_steps = upscaling_parameters.num_inference_steps

    response = requests.get(URL_API+'/superid_info', 
        headers={'Authorization': 'Bearer '+TOKEN},
        json={'id_project':id_project, 'id_image':id_image, 'scale_factor':scale_factor, 'upscaling_mode':upscaling_mode, 'strength':strength, 'num_inference_steps': num_inference_steps},
    )
    
    #print(response.content) 
    response_json = json.loads(response.text)
    print(f'response: {response_json}')
    eta = response_json.get('eta')
    credits = response_json.get('required_credits')
    width = response_json.get('width')
    height = response_json.get('height')

    return eta, credits, width, height

def get_superid_link(id_project, id_image, TOKEN):
    # get info on the upscaled image
    response = requests.get(URL_API+'/superid', 
        headers={'Authorization': 'Bearer '+TOKEN},
        json={'id_project':id_project, 'id_image':id_image},
    )
    
    #print(response.content) 
    response_json = json.loads(response.text)
    #print(f'response: {response_json}')
    link = response_json[-1].get('l')
    return link