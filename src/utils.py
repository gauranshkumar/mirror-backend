#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gauransh
"""

import subprocess as sp
from moviepy.editor import *
import os
# subprocess.check_output("which ffmpeg", shell=True).strip().decode('utf-8').strip()
# os.environ["IMAGEIO_FFMPEG_EXE"] = "ffmpeg"


class AVHandle():
    """A Utility Class for Audio/Video Operations Handle
    \npath : Path to Video File"""

    def __init__(self, path):
        self.path = path
        self.duration = 0

    def separateAudio(self):
        """Function to separate the audio from video and store it in './tmpfiles/audio.wav'"""
        audioClip = AudioFileClip(self.path)
        self.duration = int(audioClip.duration)
        print(audioClip.duration)
        audioClip.write_audiofile("./tmpfiles/audio.mp3")

    # def mergeTranslatedAudio(self, path):
    #     """Function to merge the Audio to Video
    #     \npath : Path to New Audio File"""
    #     # newAudioClip = CompositeAudioClip([AudioFileClip(path)])
    #     # videoClip = VideoFileClip(self.path)
    #     # videoClip2 = videoClip.set_audio(newAudioClip)
    #     # videoClip2.write_videofile("finalVideo.mp4")
    #     ffmpeg_log = "tmpfiles/ffmpeg_logs.txt"
    #     command = ['ffmpeg',
    #                '-y',  # approve output file overwite
    #                '-i', str(self.path),
    #                '-i', str(path),
    #                '-map', '0:v:0',
    #                '-map', '1:a:0',
    #                '-c:v', 'copy',
    #                '-c:a', 'copy',
    #                '-shortest',
    #                str("./tmpfiles/finalVideo.mp4")]

    #     with open(ffmpeg_log, 'w') as f:
    #         process = sp.Popen(command, stderr=f)

    # def trimAudio(self):
    #     if(self.duration > 300):
    #         ffmpeg_log = "tmpfiles/ffmpeg_logs.txt"
    #         command = ['ffmpeg',
    #                    '-ss', '00:00:00',
    #                    '-to', '00:05:00',
    #                    '-i', './tmpfiles/audio.mp3',
    #                    '-c', 'copy',
    #                    str("./tmpfiles/audio.wav")]

    #         with open(ffmpeg_log, 'w') as f:
    #             process = sp.Popen(command, stderr=f)

    #     else:
    #         ffmpeg_log = "tmpfiles/ffmpeg_logs.txt"
    #         command = ['ffmpeg',
    #                    '-i', './tmpfiles/audio.mp3',
    #                    str("./tmpfiles/audio.wav")]

    #         with open(ffmpeg_log, 'w') as f:
    #             process = sp.Popen(command, stderr=f)
