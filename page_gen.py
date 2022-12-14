import PIL
from PIL import Image
import os
from keyframe_extract import get_img_aesthetic_score
import cv2

width = 2400
height = 4000

def generate_page(video_name, max_width = 2):
    pages = []
    pages.append(PIL.Image.new(mode="RGB", size=(width, height), color = "white"))

    page_count = 0
    image_paths = os.listdir(video_name + "/speech_frames")

    small_width = int((width - 200 - ((max_width - 1) * 50)) / max_width)

    row_count = 0
    column_count = 0
    page_height = 0
    page = pages[0]
    for i, path in enumerate(image_paths):
        image_path = os.path.join(video_name, ("speech_frames/speechframe_" + str(i+1) + ".jpg"))
        image = Image.open(image_path)
        if row_count >= max_width:
            column_count += 1
            row_count = 0

        small_height = int((small_width / image.width) * image.height)
        image = image.resize((small_width, small_height))
        page.paste(image, (100 + row_count * small_width + 50*row_count, 100 + column_count * small_height + 50*column_count))
        row_count += 1
        page_height = 100 + column_count * small_height + 50*column_count + 100 + small_height
        
        if page_height + small_height + 150 > height and row_count == max_width:
            page = page.crop((0, 0, page.width, page_height))
            page_count += 1
            pages.append(PIL.Image.new(mode="RGB", size=(width, height), color = "white"))
            page = pages[page_count]
            row_count = 0
            column_count = 0

    
    for i, page in enumerate(pages):
        page.save('page'+str(i)+'.jpg')
