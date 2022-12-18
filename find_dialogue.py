from difflib import SequenceMatcher
import os
import re

def parse_script(script_path):
    lines = []
    with open(script_path, "r") as f:
        all_lines = f.readlines()
        lines = [line.split(':') for line in all_lines]
        for line in lines:
            line[1] = line[1][1:-1]
    return lines

def match_dialogue(dir_path,script_path):
    script_lines = parse_script(script_path)

    speech_text_path = os.path.join(dir_path, "speech_text")
    for filename in os.listdir(speech_text_path):

        file = os.path.join(speech_text_path,filename)
        f = open(file,"r+")
        speech_lines = f.readlines()

        with open(os.path.join(dir_path + "/matched_text", filename), 'w') as f1:
            previous_lines = []
            for character_line in speech_lines:
                character_line = character_line[:-1]
                closest_line = []
                best_ratio = 0
                for script_line in script_lines:
                    if (script_line[0] + ': ' + script_line[1] + '\n') not in previous_lines:
                        ratio = SequenceMatcher(None, character_line[:-1], script_line[1]).ratio()
                        if ratio > best_ratio:
                            closest_line = script_line
                            best_ratio = ratio
                new_line = closest_line[0] + ": " + closest_line[1] + "\n"
                f1.write(closest_line[0] + ": " + closest_line[1] + "\n")
                previous_lines.append(new_line)


# script_lines = parse_script("infinity_script.txt")
# match_dialogue("infinity", "infinity_script.txt")
