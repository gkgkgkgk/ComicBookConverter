import cartoon
import keyframe_extract as scene
from speech2text import speech_to_text 
from assembly_speech2text import assembly_speech2text
from utils import init_video
from find_dialogue import match_dialogue
from face_body_detect import detect_face_or_body
from add_speech import add_speech
from page_gen import generate_page

def generate(video_name, video_path, script_path=""):
<<<<<<< HEAD
    # print("Initializing Video...")
    # video = init_video(video_name)
    # print("Splitting frames and audio...")
    # scene.get_key_frames_and_audio(video_path, video, skip=10)
    # print("Cartoonizing Frames...")
    # cartoon.cartoon_img(video_name)
    # print("Converting audio to text...")
    # assembly_speech2text(video_name)
    # if script_path != "":
    #     print("Matching text to script...")
    #     match_dialogue(video_name, script_path)
    # print("Detecting Faces and People...")
=======
    print("Initializing Video...")
    video = init_video(video_name)
    print("Splitting frames and audio...")
    scene.get_key_frames_and_audio(video_path, video, skip=50)
    print("Cartoonizing Frames...")
    cartoon.cartoon_img(video_name)
    print("Converting audio to text...")
    assembly_speech2text(video_name)
    if script_path != "":
        print("Matching text to script...")
        match_dialogue(video_name, script_path)
    print("Detecting Faces and People...")
>>>>>>> 6f2a2703ebf9a2cf3dbbe4127515eb87b5901958
    body_face_locs = detect_face_or_body(video_name)
    # print("Adding Speech Bubbles...")
    # add_speech(video_name, body_face_locs)
    # print("Generating Page...")
    # generate_page(video_name)
    # print("Done!")

<<<<<<< HEAD
generate("avengers2", "videos/avengers2.mp4", script_path="scripts/avengers2_script.txt")
=======
generate("grand", "grand5.mp4", script_path="grand5_script.txt")
>>>>>>> 6f2a2703ebf9a2cf3dbbe4127515eb87b5901958
