#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gauransh
"""

import subprocess as sp
from moviepy.editor import *
import os
import requests
from lxml.html import fromstring
import speech_recognition as sr
import os
import subprocess
import wave
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pydub import AudioSegment
from ibm_watson import SpeechToTextV1
import json

recognizer = sr.Recognizer()
# subprocess.check_output("which ffmpeg", shell=True).strip().decode('utf-8').strip()
# os.environ["IMAGEIO_FFMPEG_EXE"] = "ffmpeg"


class AVHandle():
    """A Utility Class for Audio/Video Operations Handle
    \npath : Path to Video File"""

    def __init__(self, path, output_path="./tmpfiles/audio.wav"):
        self.path = path
        self.output_path = output_path
        self.duration = 0

    def separateAudio(self):
        """Function to separate the audio from video and store it in './tmpfiles/audio.wav'"""
        audioClip = AudioFileClip(self.path)
        self.duration = int(audioClip.duration)
        print(audioClip.duration)
        audioClip.write_audiofile(self.output_path, codec="pcm_s16le")
        return self.output_path

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


class SeechToText():
    def __init__(self, path):
        """
        Class to Translate the separated Audio to given language
        Parameters
        ----------
        path : str
            Path to desired audio file.
        language : str
            Language to translate to.
        Returns
        -------
        None.
        """
        self.path = path

    def speechToText(self):
        """
        Internal Function to convert the speech to Text/Transcript and store
        it in /tmpfiles/transcript.txt
        Returns
        -------
        None.
        """
        # Input audio file to be sliced
        audio = AudioSegment.from_wav("tmpfiles/audio.wav")

        # '''
        # Step #1 - Slicing the audio file into smaller chunks.
        # '''
        # Length of the audiofile in milliseconds
        n = len(audio)

        # Variable to count the number of sliced chunks
        counter = 1

        # Text file to write the recognized audio
        fh = open("transcript.txt", "w+")

        # Interval length at which to slice the audio file.
        # If length is 22 seconds, and interval is 10 seconds,
        # The chunks created will be:
        # chunk1 : 0 - 10 seconds
        # chunk2 : 10 - 20 seconds
        # chunk3 : 20 - 22 seconds
        interval = 10 * 1000

        # Length of audio to overlap.
        # If length is 22 seconds, and interval is 10 seconds,
        # With overlap as 1.5 seconds,
        # The chunks created will be:
        # chunk1 : 0 - 10 seconds
        # chunk2 : 8.5 - 18.5 seconds
        # chunk3 : 16 - 22 secondsreturn translatedText
        end = 0
        overlap = 1.2 * 1000

        # Flag to keep track of end of file.
        # When audio reaches its end, flag is set to 1 and we break
        flag = 0

        # Creating directory to store audio chunks
        try:
            os.mkdir('audio_chunks')
        except(FileExistsError):
            pass

        # Iterate from 0 to end of the file,
        # with increment = interval
        for i in range(0, 2 * n, interval):

            # During first iteration,
            # start is 0, end is the interval
            if i == 0:
                start = 0
                end = interval

            # All other iterations,
            # start is the previous end - overlap
            # end becomes end + interval
            else:
                start = end - overlap
                end = start + interval

            # When end becomes greater than the file length,
            # end is set to the file length
            # flag is set to 1 to indicate break.
            if end >= n:
                end = n
                flag = 1

            # Storing audio file from the defined start to end
            chunk = audio[start:end]

            # Filename / Path to store the sliced audio
            filename = 'audio_chunks/chunk'+str(counter)+'.wav'

            # Store the sliced audio file to the defined path
            chunk.export(filename, format="wav")
            # Print information about the current chunk
            print("Processing chunk "+str(counter)+". Start = "
                  + str(start)+" end = "+str(end))

            # Increment counter for the next chunk
            counter = counter + 1

            # Slicing of the audio file is done.
            # Skip the below steps if there is some other usage
            # for the sliced audio files.

        # '''
        # Step #2 - Recognizing the chunk and writing to a file.
        # '''

            # Here, Google Speech Recognition is used
            # to take each chunk and recognize the text in it.

            # Specify the audio file to recognize

            AUDIO_FILE = filename

            # Initialize the recognizer
            r = sr.Recognizer()

            # Traverse the audio file and listen to the audio
            with sr.AudioFile(AUDIO_FILE) as source:
                # r.adjust_for_ambient_noise(source)
                audio_listened = r.listen(source)

            # Try to recognize the listened audio
            # And catch expections.
            try:
                # rec = r.recognize_google(audio_listened)

                rec = r.recognize_wit(
                    audio_data=audio_listened, key="N2MTVJ52GLZ5H4HDR275SR5IOCKYIRUL")

                # If recognized, write into the file.
                print("Recognised : {}".format(rec))
                fh.write(rec+" ")

            # If google could not understand the audio
            except sr.UnknownValueError:
                print("Could not understand audio")

            # If the results cannot be requested from Google.
            # Probably an internet connection error.
            except sr.RequestError as e:
                print("Could not request results.")

            # Check for flag.
            # If flag is 1, end of the whole audio reached.
            # Close the file and break.
            if flag == 1:
                fh.close()
                break

    def speechToTextIBM(self):
        r = sr.Recognizer()
        w = open("transcript.txt", "w+")
        authenticator = IAMAuthenticator(
            'QamXe_2ysB-t6PUa1jOatSUPShJECAZeqOE_OM6-tV4e')
        speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )
        speech_to_text.set_service_url(
            'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/ae8c5aa3-151f-4a35-8f1a-05676a1379e1')
        with open(self.path, 'rb') as audio_file:
            speech_recognition_results = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav'
            ).get_result()
        for result in speech_recognition_results['results']:
            for alternative in result['alternatives']:
                w.write(alternative['transcript'])
                print(alternative['transcript'])
                return alternative['transcript']
