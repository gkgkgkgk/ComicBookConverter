import cartoon
import keyframe_extract as scene
from speech2text import speech_to_text 
from utils import init_video

# video = init_video("frisch")
# frames_dir = scene.get_key_frames_and_audio("videos/frisch.mp4", video, skip=3)
# cartoon.cartoon_img(frames_dir)
# speech_to_text(video)

video_name = "avengers"
# init_video(video_name)
# frames_dir = scene.get_key_frames_and_audio("videos/avengers.mp4", video_name, skip=3)
# cartoon.cartoon_img(frames_dir)
speech_to_text(video_name)