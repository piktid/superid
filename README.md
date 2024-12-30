<p align="center">
  <img src="https://studio.piktid.com/logo.svg" alt="SuperID by PiktID logo" width="150">
  </br>
  <h3 align="center"><a href="[https://studio.piktid.com](https://studio.piktid.com)">SuperID by PiktID</a></h3>
</p>


# SuperID 3.1.0
[![Official Website](https://img.shields.io/badge/Official%20Website-piktid.com-blue?style=flat&logo=world&logoColor=white)](https://piktid.com)
[![Discord Follow](https://dcbadge.vercel.app/api/server/FJU39e9Z4P?style=flat)](https://discord.com/invite/FJU39e9Z4P)

SuperID is GenAI upscaler, particularly suitable for portrait photos. 
It is based on GANs, transformers and diffusion models, rendering it extremely powerful in adding missing details.

[![SuperID examples](http://i3.ytimg.com/vi/0UKFPpC50m0/hqdefault.jpg)](https://www.youtube.com/watch?v=0UKFPpC50m0)


## About
SuperID utilizes generative models to intelligently upscale your photos. It can be extremely powerful in the following scenarios:

- <ins>Close-up portrait photos</ins>: Since the generative models behind SuperID are trained on human faces, the AI performs better when a single face is provided as input.
- <ins>Small thumbnails</ins>: When the photo to upscale is at very low resolution (e.g. 128x128), SuperID can add missing details. 
- <ins>Photos with noise and JPEG artifacts</ins>: SuperID can effectively denoise and remove artifacts from your photos.
- <ins>Images with transparent backgrounds</ins>: SuperID intelligently upscale PNG images (e.g. logos) with transparent backgrounds.

## Getting Started
<a target="_blank" href="https://colab.research.google.com/drive/1DBjyDcwrZBzFPFCDjRnmNHBt2mEqxW6D?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

The following instructions suppose you have already installed a recent version of Python. For a general overview, please visit the <a href="https://api.piktid.com/docs">API documentation</a>.
To use any PiktID API, an access token is required. 

> **Step 0** - Register <a href="https://studio.piktid.com">here</a>. 10 credits are given for free to all new users.

> **Step 1** - Clone the SuperID library
```bash
# Installation commands
$ git clone https://github.com/piktid/superid.git
$ cd superid
$ pip install -r requirements.txt
```

> **Step 2** - Export the email and password as environmental variables
```bash
$ export SUPERID_EMAIL={Your email here}
$ export SUPERID_PASSWORD={Your password here}
```

> **Step 3** - Change in main.py the URL of the image to be upscaled
```python
...
url = 'your-url'
...
```

> **Step 4** - Run the main function
```bash
$ python3 main.py
```

Without any additional argument, SuperID upscales the image times 2 and provides the result asynchronously. 
If you want to change the output resolution, format or retrieval method, use the following general command:

```bash
$ python3 main.py --scale_factor '2' --output_format 'PNG' --email
```

- **scale_factor**: Select the upscaling factor: upscale time 2 or times 4
- **output_format**: Save the upscaled image in PNG or JPEG
- **email**: Get the output link via email once ready


## Face fixer
It is now possible to automatically enhance little faces in photos while upscaling the input. To do so, add the flag:

```bash
$ python3 main.py --face_fixer
```

## Image denoising (coming soon)
It is also possible to reduce the noise in the original photo by playing with the parameter (range 0-1), as in the example:

```bash
$ python3 main.py --denoise_input '0.5'
```

## Creative upscaling (for advanced users)
To modify the capabilities of SuperID towards more conservative or creative outputs, control the upscaling process through the generative parameters as follows:

```bash
$ python3 main.py --prompt '' --prompt_strength '0.35' --controlnet_scale '0.5' --seed 0
```

- **prompt**: Describe your image
- **prompt_strength**: The lower the more similar to the input image, the higher, the more diverse (range 0-1)
- **guidance_scale**: How much to follow the prompt description (range 1-10)
- **controlnet_scale**: The higher, the more the upscaling will follow the lines of the input image (range 0-1)
- **seed**: Choose a seed to replicate the results

## Fast upscaling (coming soon)
When the output quality is not the main priority, we allow users to opt for a fast upscaling process via the command:

```bash
$ python3 main.py --fast
```

## Contact
office@piktid.com
