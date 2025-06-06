<p align="center">
  <img src="https://studio.piktid.com/logo.svg" alt="SuperID by PiktID logo" width="150">
  </br>
  <h3 align="center"><a href="[https://studio.piktid.com](https://studio.piktid.com)">SuperID by PiktID</a></h3>
</p>


# SuperID 3.2.0
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
- <ins>Images with transparent backgrounds</ins>: SuperID intelligently upscales PNG images (e.g. logos) with transparent backgrounds.

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

> **Step 3** - Run the main function with the URL of the image or a local file path to be upscaled
```bash
# Using a URL
$ python3 main.py --url 'your-url'

# Using a local file path
$ python3 main.py --filepath '/path/to/your/image.jpg'
```

Without any additional argument, SuperID upscales the image times 2 and provides the result asynchronously. 
If you want to change the output resolution, format or retrieval method, use the following general command:

```bash
# Using a URL
$ python3 main.py --url 'your-url' --scale_factor '2' --output_format 'PNG' --email

# Using a local file path
$ python3 main.py --filepath '/path/to/your/image.jpg' --scale_factor '2' --output_format 'PNG' --email
```

- **scale_factor**: Select the upscaling factor: upscale times 1, 2 or 4
- **output_format**: Save the upscaled image in PNG or JPEG
- **email**: Get the output link via email once ready

---

# Super Mode (Default)

The default mode uses advanced generative AI models for high-quality results. This mode supports creative control parameters and detailed customization options.

## Creative upscaling
To modify the capabilities of SuperID towards more conservative or creative outputs, control the upscaling process through the generative parameters:

```bash
# Using a URL
$ python3 main.py --url 'your-url' --prompt '' --creativity 7 --fractality 3 --fidelity 5 --seed 0

# Using a local file path
$ python3 main.py --filepath '/path/to/your/image.jpg' --prompt '' --creativity 7 --fractality 3 --fidelity 5 --seed 0
```

- **prompt**: Describe your image
- **creativity**: The lower the more similar to the input image, the higher, the more diverse (range 1-20)
- **fractality**: How much to follow the prompt description (range 1-20)
- **fidelity**: The higher, the more the upscaling will follow the resemblance of the input image (range 0-20)
- **seed**: Choose a seed to reproduce the results

## Face enhancer
Manually enable face enhancement when needed:

```bash
$ python3 main.py --filepath '/path/to/your/image.jpg' --face_enhancer
```

## Image denoising
You can reduce the noise in the original photo by adjusting the denoise parameter (range 0-20):

```bash
$ python3 main.py --filepath '/path/to/your/image.jpg' --denoise 10
```

## Image enhancement options
Control additional image processing filters in Super mode:

```bash
# Disable automatic image filters
$ python3 main.py --filepath '/path/to/your/image.jpg' --no_image_filters

# Disable color matching
$ python3 main.py --filepath '/path/to/your/image.jpg' --no_match_colors
```

---

# Fast Mode

A speed-optimized mode that prioritizes processing time over advanced AI features. When speed is a priority and you need quick results, use the fast upscaling mode:

```bash
$ python3 main.py --filepath '/path/to/your/image.jpg' --fast
```

**Note:** Creative control parameters (prompt, creativity, fractality, fidelity, denoise) are not available in fast mode.

## Face enhancer
Fast mode automatically applies smart face enhancement. However, the algorithm may sometimes decide not to apply it. In such cases, you can force face enhancement to override the internal decision:

```bash
# Fast mode with automatic face enhancement (default behavior)
$ python3 main.py --filepath '/path/to/your/image.jpg' --fast

# Fast mode with forced face enhancement (overrides algorithm decision)
$ python3 main.py --filepath '/path/to/your/image.jpg' --fast --force_face_enhancer
```

## Image enhancement options
Control additional image processing filters in Fast mode:

```bash
# Disable automatic image filters
$ python3 main.py --filepath '/path/to/your/image.jpg' --fast --no_image_filters

# Disable color matching
$ python3 main.py --filepath '/path/to/your/image.jpg' --fast --no_match_colors
```

---

## Contact
office@piktid.com
