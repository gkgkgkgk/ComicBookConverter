import speech_recognition as sr
import os

def speech_to_text(dir_path):
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    for i, audio in enumerate(os.listdir(dir_path + "/audio")):
        aud_path = os.path.join(dir_path, ("audio/audio_scene_" + str(i+1) + ".wav"))

        try:
            with sr.AudioFile(aud_path) as source:
                audio_text = r.listen(source)

            text = r.recognize_google(audio_text)

            with open(os.path.join(dir_path + "/text", "text_" + str(i+1)) + ".txt", 'w') as f:
                f.write(text)

        except:
            print("no words!")
            continue