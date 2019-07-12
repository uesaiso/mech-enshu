# -*- coding: utf-8 -*-
from multiprocessing import Process, Value, Manager
from ctypes import c_char_p


from video import video_capture
from voice import voice_to_text


if __name__ == "__main__":
    manager = Manager()
    break_flag = Value("i", 1)
    text = manager.Value(c_char_p, "")

    koekatamarin = Koekaramarin()
    p1 = Process(target=voice_to_text, args=(text, break_flag))
    p2 = Process(target=video_capture, args=(text, break_flag))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("end")
