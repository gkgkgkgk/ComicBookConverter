from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
import os

def add_speech(video_name, locs):
    for i, text_path in enumerate(os.listdir(video_name + "/matched_text")):
        text_file = open(video_name + "/matched_text/" + text_path, "r")
        text = text_file.read()
        image_path = video_name + "/cartoon_frames/keyframe_scene_"+str(i+1)+".jpg"

        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        wh = (img.width, img.height)
        if text != "":
            create_bubble(draw, text, locs[i], wh)
        img.save(video_name + '/speech_frames'+'/speechframe_'+str(i)+'.jpg')

def create_bubble(draw, text, loc, wh):
    font = ImageFont.truetype("lib/fonts/Comic Book.otf", 24)
    wrapped = textwrap.wrap(text, width=30)
    if len(wrapped) == 0:
        wrapped.append(text)

    font_bbox = list(font.getmask(wrapped[0]).getbbox())
    for i in range(1, len(wrapped)):
        bbox = font.getmask(wrapped[i]).getbbox()

        if abs(bbox[0] - bbox[2]) > abs(font_bbox[0] - font_bbox[2]):
            font_bbox[0] = bbox[0]
            font_bbox[2] = bbox[2]
        
        if abs(bbox[1] - bbox[3]) > abs(font_bbox[1] - font_bbox[3]):
            font_bbox[1] = bbox[1]
            font_bbox[3] = bbox[3]
    
    font_height = abs(font_bbox[1] - font_bbox[3])
    position = get_position(loc, wh, (abs(font_bbox[0] - font_bbox[2]), font_height*(len(wrapped) + 1)))

    draw.rounded_rectangle([(position[0] - 20, position[1] - 20), (20 + position[0] + abs(font_bbox[0] - font_bbox[2]), 20 + position[1] + font_height*(len(wrapped) + 1))], radius=0, fill="white", outline ="black", width = 2)

    for i, line in enumerate(wrapped):
        draw.text((position[0], position[1] + (i * font_height)),line,(0,0,0),font=font)

def get_position(loc, img_wh, wh):
    min_box = [1000000,1000000,0,0]
    for face in loc[0]:
        if face[0] < min_box[0]:
            min_box[0] = face[0]
        if face[1] < min_box[1]:
            min_box[1] = face[1]
        if face[2] > min_box[2]:
            min_box[2] = face[2]
        if face[3] > min_box[3]:
            min_box[3] = face[3]
    for person in loc[1]:
        if person[0] < min_box[0]:
            min_box[0] = person[0]
        if person[1] < min_box[1]:
            min_box[1] = person[1]
        if person[2] > min_box[2]:
            min_box[2] = person[2]
        if person[3] > min_box[3]:
            min_box[3] = person[3]

    x = 0
    if min_box[0] > wh[0]:
        x = min_box[0] - wh[0]
    elif img_wh[0] - min_box[2] > wh[0]:
        x = min_box[2]
    else:
        x = min_box[0]
    
    y = 0
    if min_box[1] > wh[1]:
        y = min_box[1] - wh[1]
    elif img_wh[1] - min_box[3] > wh[1]:
        y = min_box[2]
    else:
        y = min_box[1]
    
    return (x,y)

