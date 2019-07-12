# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


class Koekaramarin:
    def __init__(self):
        self.font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc", 32)

    def embody(self, frame, text, mouth_position):
        if text:
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text(mouth_position, text, font=self.font, fill=(0, 0, 255))
            frame = np.array(img_pil)
        cv2.imshow("Koekaramarin", frame)


class MouthDetector:
    def __init__(self):
        self.mouth_cascade = cv2.CascadeClassifier(
            "./cascade_files/haarcascade_mcs_mouth.xml"
        )

    def detect(self, frame):
        ans = (20, 50)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mouth_rects = self.mouth_cascade.detectMultiScale(gray, 1.7, 11)
        for (x, y, w, h) in mouth_rects:
            y = int(y - 0.15 * h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            ans = (x + w / 2, y + h / 2)
            break
        cv2.imshow("Mouth Detect", frame)
        return ans


def video_capture(text, break_flag):
    cap = cv2.VideoCapture(0)
    koekatamarin = Koekaramarin()
    mouth_detector = MouthDetector()

    while break_flag.value:
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
        cv2.imshow("Raw Frame", frame)

        mouth_position = mouth_detector.detect(frame.copy())

        koekatamarin.embody(frame.copy(), text.value, mouth_position)

        k = cv2.waitKey(1)
        if k == 27:
            break_flag.value = 0
    cap.release()
    cv2.destroyAllWindows()
