# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


class Koekaramarin:
    def __init__(self):
        self.font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc", 32)

    def embody(self, frame, text):
        if text:
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text((20, 50), text, font=self.font, fill=(200, 0, 0))
            frame = np.array(img_pil)
        return frame


def video_capture(text, break_flag):
    cap = cv2.VideoCapture(0)
    koekatamarin = Koekaramarin()

    while break_flag.value:
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
        cv2.imshow("Raw Frame", frame)

        edframe = koekatamarin.embody(frame, text.value)

        cv2.imshow("Koekaramarin", edframe)

        k = cv2.waitKey(1)
        if k == 27:
            break_flag.value = 0
    cap.release()
    cv2.destroyAllWindows()
