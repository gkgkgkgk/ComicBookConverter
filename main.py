import argparse
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
    print(script_path)
    print("Initializing Video...")
    video = init_video(video_name)
    print("Splitting frames and audio...")
    scene.get_key_frames_and_audio(video_path, video, skip=50)
    print("Cartoonizing Frames...")
    cartoon.cartoon_img(video_name)
    print("Converting audio to text...")
    assembly_speech2text(video_name)
    if script_path != None and script_path != "":
        print("Matching text to script...")
        match_dialogue(video_name, script_path)
    print("Detecting Faces and People...")
    body_face_locs = detect_face_or_body(video_name)
    print("Adding Speech Bubbles...")
    add_speech(video_name, body_face_locs)
    print("Generating Page...")
    generate_page(video_name)
    print("Done!")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("video_name", help="Name of the video")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--script_path", help="Path to the script file (optional)")
    args = parser.parse_args()

    # Call the generate function with the parsed arguments
    generate(args.video_name, args.video_path, script_path=args.script_path)