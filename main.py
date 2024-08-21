import fitz
import requests
import os


def convert_to_speech(text, voice="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs"
                                  "/manifest.json"):
    url = "https://api.play.ht/api/v2/tts/stream"

    data = {
        "voice_engine": 'PlayHT2.0-turbo',
        "text": text,
        "voice": voice,
        "output_format": "mp3",
        "sample_rate": "44100",
        "speed": 1,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": os.environ.get("AUTHORIZATION"),
        "X-USER-ID": os.environ.get("X-USER-ID"),
    }
    # create audio URL
    response = requests.post(url=url, json=data, headers=headers)
    audio_url = response.json()["href"]
    # open audio URL
    response = requests.get(url=audio_url, headers=headers, stream=True)
    response.raise_for_status()
    return response


# convert pdf to string
def pdf_to_string(file):
    doc = fitz.open(file)
    pdf_text = ""
    for page in doc:
        pdf_text += page.get_text()
    return pdf_text


#  load pdf to string and convert to audio
filename = "example.pdf"
pdf = pdf_to_string(filename)
audio_link = convert_to_speech(pdf)

# download audio from URL
with open("audio.mp3", 'wb') as audio:
    for chunk in audio_link.iter_content(chunk_size=1024):
        # writing one chunk at a time to pdf file
        if chunk:
            audio.write(audio_link.content)
