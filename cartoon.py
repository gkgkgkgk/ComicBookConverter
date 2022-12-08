from lib import cartoonize
import os
from PIL import Image, ImageEnhance

def cartoon_img(folder, output_folder="cartoon_images"):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    cartoonize.cartoonize(folder, output_folder, "lib/saved_models")

    for filename in os.listdir(output_folder):
        path = os.path.join(output_folder, filename)
        im = Image.open(path)
        enhancer = ImageEnhance.Contrast(im)
        im_output = enhancer.enhance(1.35)
        im_output.save(path)