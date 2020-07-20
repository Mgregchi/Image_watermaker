# USAGE
# python watermarking.py --watermark --folder  --coordinates
from PIL import Image
import argparse
import os
import sys
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--watermark", required=True,
                help="path to input image to be the watermark ")
ap.add_argument("-i", "--images", required=True,
                help="path to folder containing images to add watermark on")
ap.add_argument("-c", "--coordinates", default='C',
                help="""where to place watermark on image(s).
TR for top right
TL for top left
BR for bottom right
BL for bottom left
C for center which is default if none is provided
""")
args = vars(ap.parse_args())

# Program rules
# Image size standards
# Can be changed if need be
WATERMARK_H = 80
WATERMARK_W = 140

# Image Size standard
# The size can be edited to suit your program
STANDARD = 320
UNSUPPORTED_FILES = []

# this makes sure folder is created in the CWD   
os.chdir(str(args['images']))

created_folder = 'watermaked_images'
os.makedirs(created_folder, exist_ok=True)
# load the watermark, get height, width
try:
    watermark = Image.open(args['watermark'])

except FileNotFoundError as err:
    raise Exception(err)
# Check if watermark has alpha value, add if it does not
# by converting to RGBA
if watermark.mode  == 'RGB':
    watermark = watermark.convert('RGBA')
watermarkWidth, watermarkHeight = watermark.size

# Match the watermark Width and Height with STANDARD
if watermarkWidth > WATERMARK_W or watermarkHeight > WATERMARK_H:
    watermark = watermark.resize((138, 77))


# walk image directory
for filename in os.listdir(args['images']):
    if not (filename.endswith('.jpg') or filename.endswith('.png')) or filename == watermark:
        continue # Skip non_image files and the watermark file itself

    try:
        im = Image.open(filename)
        width, height = im.size
    except:
        print('File not supported and is skiped')
    if width > STANDARD and height > STANDARD:
        if not width > STANDARD: # Some images tends to have higher width than height
            watermark = watermark.resize((int(watermarkWidth - 15), 0)) # We resize watermark width to fit image width

            # setup the coordinates
            # Calculation for the image pixels coordinates
        top_left = 0,0
        top_right = width - watermarkWidth - 5, height - watermarkHeight - 5
        bottom_left = -0 , height - watermarkHeight - 5
        Default = int(width /2 - watermarkWidth /2), int(height / 2 - watermarkHeight / 2)
        bottom_right = width - watermarkWidth - 5, height - watermarkHeight - 5

        # Reasign them the coordinates values for user coordinates option
        coordinate = {'TL': top_left, 'TR': top_right, 'BR': bottom_right, 'BL': bottom_left, 'C': Default}
        watermark_Coordinates = coordinate.get(args['coordinates'], Default)
        try:
            # paste watermark to coordinates provided
            im.paste(watermark, (watermark_Coordinates), watermark) # The 3rd arg can be removed if PIL raise
            im.save(os.path.join(created_folder, filename))                     # KeyError for transparncy issues
        except OSError as err:
            print(str(err))


