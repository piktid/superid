<p align="center">
  <img src="https://studio.piktid.com/logo.svg" alt="SuperID by PiktID logo" width="150">
  </br>
  <h3 align="center"><a href="[https://studio.piktid.com](https://studio.piktid.com)">SuperID by PiktID</a></h3>
</p>


# SuperID 3.0.1
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

Without any additional argument, SuperID utilizes the "super" method and provides the result asynchronously. 
If you want to upscale x2, use the following general command:

```bash
$ python3 main.py --upscaler_type '4' --scale_factor '2' --output_format 'PNG' --flag_email True --prompt '' --prompt_strength '0.35' --controlnet_scale '0.5' --num_inference_steps 20 --seed 0
```

- **upscaler_type**: Select which upscaler to use: 0 (None), 1 (Soft Portrait), 2 (Hard Portrait), 3 (Mix), 4 (Best overall)
- **upscaling_mode**: Select the upscaling mode: fast (takes few seconds, lower quality, not available at the moment), super (takes up to minutes, higher quality overall)
- **scale_factor**: Select the upscaling factor: upscale time 2 or times 4
- **output_format**: Save the upscaled image in PNG or JPEG
- **flag_email**: Get the output link via email once ready
- **prompt**: Describe your image
- **prompt_strength**: The lower the more similar to the input image, the higher, the more diverse (range 0-1)
- **guidance_scale**: How much to follow the description
- **controlnet_scale**: The higher, the more the upscaling will follow the lines of the input image (range 0-1)
- **num_inference_steps**: The higher, the more denoising steps
- **seed**: Choose a seed to replicate the results

## Contact
office@piktid.com
