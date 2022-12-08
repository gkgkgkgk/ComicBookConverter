from difflib import SequenceMatcher
import os

def parse_script(script_path):
    lines = []
    with open(script_path, "r") as f:
        all_lines = f.readlines()
        lines = [line.split(':') for line in all_lines]
        for line in lines:
            line[1] = line[1][1:-1]

    return lines

def get_dialogue(text_dir, lines):

    for filename in os.listdir(text_dir):
        file = os.path.join(text_dir,filename)
        f = open(file,"r+")
        speech_line = f.readline()
        closest_line = []
        best_ratio = 0

        for line in lines:
            ratio = SequenceMatcher(None, speech_line, line[1]).ratio()
            if ratio > best_ratio:
                closest_line = line
                best_ratio = ratio

        f.write("\n" + closest_line[0] + ": " + closest_line[1])

get_dialogue("grand/text", parse_script("grand_script.txt"))
# print(similar("chocolate fountain", "Oh! Idea! Chocolate Fountains."))