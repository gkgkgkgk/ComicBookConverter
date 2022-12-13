import requests
import json
import os
api_key = "01de63cb44c24ab38577d8fc7d9ac13b"

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def assembly_speech2text(dir_path):

    for i, audio in enumerate(os.listdir(dir_path + "/audio")):
        aud_path = os.path.join(dir_path, ("audio/audio_scene_" + str(i+1) + ".wav"))

        # Convert wav file to URL
        headers = {'authorization': api_key}
        response = requests.post('https://api.assemblyai.com/v2/upload',
                        headers=headers,
                        data=read_file(aud_path))
        url = response.json()['upload_url']

        # Send URL to be transcibed and get the request id
        endpoint = "https://api.assemblyai.com/v2/transcript"
        json = { "audio_url": url, "speaker_labels": True}
        headers = {
            "authorization": api_key,
            "content-type": "application/json"
        }
        response = requests.post(endpoint, json=json, headers=headers)
        id = response.json()["id"]

        # Wait for transcription to be finished
        endpoint = "https://api.assemblyai.com/v2/transcript/" + id
        headers = {
            "authorization": api_key,
        }
        print("Transcribing Scene " + str(i) + "...")
        status = "processing"
        while status == "processing":
            response = requests.get(endpoint, headers=headers)
            status = response.json()["status"]

        # Write each line said by a different person to corresponding scene text file
        if response.json()["utterances"]:
            with open(os.path.join(dir_path + "/speech_text", "text_" + str(i+1)) + ".txt", 'w') as f:
                for speaker in response.json()["utterances"]:
                    f.write(speaker["text"] + "\n")


