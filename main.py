# -*- coding: utf-8 -*-
import os
import speech_recognition
import pyaudio
import wave
import cv2
import asyncio
import threading
import time

RECORD_SECONDS = 3
FILENAME = "record.wav"
iDeviceIndex = 0
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2 ** 11
API_KEY = os.getenv("API_KEY")

global text
global break_flag
global cap
text = ""
break_flag = True
cap = cv2.VideoCapture(0)


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
    global text
    try:
        r = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(FILENAME) as src:
            audio = r.record(src)
        text = r.recognize_google(audio, key=API_KEY, language="ja-JP")
    except speech_recognition.UnknownValueError:
        text = ""
    print(text)


def record_loop():
    global break_flag
    while break_flag:
        record()
        recognition()


def opencv_loop():
    global text
    global break_flag
    global cap
    while break_flag:
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
        cv2.imshow("Raw Frame", frame)
        k = cv2.waitKey(1)
        if k == 27:
            break_flag = False


if __name__ == "__main__":
    # t1 = threading.Thread(target=record_loop)
    # t2 = threading.Thread(target=opencv_loop)
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    cap.release()
    cv2.destroyAllWindows()
    print("end")
