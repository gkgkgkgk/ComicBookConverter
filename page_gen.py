import PIL
from PIL import Image
import os
from keyframe_extract import get_img_aesthetic_score
import cv2

def generate_page(video_name, max_width = 2):
    page = PIL.Image.new(mode="RGB", size=(2400, 4000), color = "white")

    image_paths = os.listdir(video_name + "/speech_frames")

    scores = []
    for path in image_paths:
        scores.append(get_img_aesthetic_score(cv2.imread(video_name + "/speech_frames/" + path), video_name + "/speech_frames/" + path))

    small_width = int((2400 - 200 - ((max_width - 1) * 50)) / max_width)

    row_count = 0
    column_count = 0
    page_height = 0
    for i, path in enumerate(image_paths):
        image = Image.open(video_name + "/speech_frames/" + path)
        if row_count >= max_width:
            column_count += 1
            row_count = 0

        small_height = int((small_width / image.width) * image.height)
        image = image.resize((small_width, small_height))
        page.paste(image, (100 + row_count * small_width + 50*row_count, 100 + column_count * small_height + 50*column_count))
        row_count += 1
        page_height = 100 + column_count * small_height + 50*column_count + 100 + small_height

    print(page_height)
    page = page.crop((0, 0, page.width, page_height))
    page.save('page.jpg')
