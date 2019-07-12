# -*- coding: utf-8 -*-
import os
import speech_recognition
import pyaudio
import wave

RECORD_SECONDS = 3
FILENAME = "record.wav"
iDeviceIndex = 0
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2 ** 11
API_KEY = os.getenv("API_KEY")


def record():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=iDeviceIndex,
        frames_per_buffer=CHUNK,
    )
    print("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finish recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(FILENAME, "wb")
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b"".join(frames))
    waveFile.close()


def recognition():
    try:
        r = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(FILENAME) as src:
            audio = r.record(src)
        text = r.recognize_google(audio, key=API_KEY, language="ja-JP")
    except speech_recognition.UnknownValueError:
        text = ""
    print(text)
    return text


def voice_to_text(text, break_flag):
    while break_flag.value:
        record()
        text.value = recognition()
