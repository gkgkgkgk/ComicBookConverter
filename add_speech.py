from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
import os

def add_speech(video_name, locs):
    text_dir = "speech_text"
    if len(os.listdir(video_name + "/matched_text")) > 0:
        text_dir = "matched_text"

    for i in range(len(os.listdir(video_name + "/cartoon_frames"))):
        path = video_name + "/"+text_dir+"/text_" + str(i+1) + ".txt"
        image_path = video_name + "/cartoon_frames/keyframe_scene_"+str(i+1)+".jpg"
        img = Image.open(image_path)
        if os.path.exists(path):
            text_file = open(path, "r")
            text = text_file.read()

            draw = ImageDraw.Draw(img)
            wh = (img.width, img.height)

            lines = text.split('\n')
            lines = [value for value in lines if value != ""]

            if len(lines) == 1:
                create_bubble(draw, lines[0], locs[i], wh, 0)

            else:
                pos = (50, 50)
                for j, line in enumerate(lines):
                    pos = create_bubble(draw, line, locs[i], wh, j, seq=True, pos=pos, total_lines=len(lines))

        img.save(video_name + '/speech_frames'+'/speechframe_'+str(i+1)+'.jpg')

def create_bubble(draw, text, loc, wh, index, seq=False, pos=(50,50), total_lines=0):
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
    
    if seq == False:
        position = get_position(loc, wh, (abs(font_bbox[0] - font_bbox[2]), font_height*(len(wrapped) + 1)))
    else:
        if index != 0:
            position = (pos[0], pos[1] + 4 * font_height + 40)
        else:
            position = get_position(loc, wh, (abs(font_bbox[0] - font_bbox[2]), font_height*(total_lines + 1)))

    draw.rounded_rectangle([(position[0] - 20, position[1] - 20), (20 + position[0] + abs(font_bbox[0] - font_bbox[2]), 20 + position[1] + font_height*(len(wrapped) + 1))], radius=0, fill="white", outline ="black", width = 2)

    for i, line in enumerate(wrapped):
        draw.text((position[0], position[1] + (i * font_height)),line,(0,0,0),font=font)
    
    print(position)
    return position

def get_position(loc, img_wh, wh):
    min_box = [1000000,1000000,0,0]

    if len(loc[0]) > 0:
        for face in loc[0]:
            if face[0] < min_box[0]:
                min_box[0] = face[0]
            if face[1] < min_box[1]:
                min_box[1] = face[1]
            if face[2] > min_box[2]:
                min_box[2] = face[2]
            if face[3] > min_box[3]:
                min_box[3] = face[3]
    if len(loc[1]) > 0:
        for person in loc[1]:
            if person[0] < min_box[0]:
                min_box[0] = person[0]
            if person[1] < min_box[1]:
                min_box[1] = person[1]
            if person[2] > min_box[2]:
                min_box[2] = person[2]
            if person[3] > min_box[3]:
                min_box[3] = person[3]

    print(len(loc[1]), len(loc[0]))
    if len(loc[1]) == 0 and len(loc[0]) == 0:
        return (50, 50)

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
    
    return (max(x, 30),max(y, 30))

