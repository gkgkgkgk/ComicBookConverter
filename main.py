import cartoon
import keyframe_extract as scene
from speech2text import speech_to_text 
from assembly_speech2text import assembly_speech2text
from utils import init_video
from find_dialogue import match_dialogue

video_name = "grand_test"
video = init_video(video_name)
scene.get_key_frames_and_audio("grand2.mp4", video, skip=10)
cartoon.cartoon_img(video_name)
assembly_speech2text(video_name)
match_dialogue(video_name, "grand2_script.txt")
