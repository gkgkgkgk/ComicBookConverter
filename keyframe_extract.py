from scenedetect import detect, ContentDetector
import cv2
import pyaesthetics
from pyaesthetics.faceDetection import getFaces
from pyaesthetics.brightness import relativeLuminance_BT709, relativeLuminance_BT709, sRGB2RGB
import tqdm
import os
import moviepy.editor as mp
from pydub import AudioSegment
import shutil
import stat

def get_img_aesthetic_score(frame, path):
    score = 0
    results = pyaesthetics.analysis.analyzeImage(path, method="fast") #perform all the availabe analysis using standard parameters
    #print(results)
    #print(relativeLuminance_BT709(sRGB2RGB(frame)))
    for key in results:
        if(key == "Text"):
            continue
        score += results[key]
    score += len(getFaces(frame))
    return score/5

def get_key_frames_and_audio(vid_path, out_folder, skip = 1):
    video = cv2.VideoCapture(vid_path)
    clip = mp.VideoFileClip(vid_path)
    clip.audio.write_audiofile(out_folder+"/temp/aud.wav")
    audio = AudioSegment.from_wav(out_folder+"/temp/aud.wav")

    scene_list = detect(vid_path, ContentDetector())
    print("Pyscene found " + str(len(scene_list)) + " scenes")

    for i, scene in enumerate(scene_list):
        print('\nScene %2d: Start %s / Frame %d, End %s / Total Frames: %d' % (
            i+1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames()-1,))

        start = int(float(scene[0].get_timecode().split(":")[2])*1000)
        end = int(float(scene[1].get_timecode().split(":")[2])*1000)
        trim = audio[start:end]
        trim.export(os.path.join(out_folder, os.path.join("audio", ("audio_scene_" + str(i+1) + ".wav"))), format="wav")

        best_score = 0
        best_frame = []
        
        for j in tqdm.tqdm(range(scene[0].get_frames(),scene[1].get_frames(), skip)):
            video.set(cv2.CAP_PROP_POS_FRAMES, j)
            _, frame = video.read()
            cv2.imwrite(out_folder+"/temp/temp.jpg", frame)

            score = get_img_aesthetic_score(frame, out_folder+"/temp/temp.jpg")
            if score > best_score:
                best_frame = frame
                best_score = score
        
        cv2.imwrite(os.path.join(out_folder, os.path.join("frames", ("keyframe_scene_" + str(i+1) + ".jpg"))), best_frame)

    return out_folder + "/frames"