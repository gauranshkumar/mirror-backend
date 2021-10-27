from utils import AVHandle, SeechToText
import language_tool_python
from pyAudioAnalysis import audioBasicIO
import soundfile as sf
import pyloudnorm as pyln
from collections import Counter


class AudioAnalyzer:
    def __init__(self, path):
        self.av = AVHandle(path)
        self.output_path = self.av.separateAudio()
        self.speech = SeechToText()
        self.transcript = self.speech.speechToTextIBM(self.output_path)

    def check_grammer(self):
        """Return the wrong grammer count"""
        wrongGrammer = language_tool_python.check(
            self.transcript, language_tool_python.LanguageTool('en-US'))
        self.misspelledWordList = [
            i.matchedText for i in wrongGrammer if i.ruleIssueType == 'misspelling']
        return len(wrongGrammer)

    def misspelled_words(self):
        """Return the misspelled words"""
        return self.misspelledWordList

    def most_common_words(self):
        """Return the most common words"""
        mcw_list = Counter(self.transcript.split()).most_common(5)
        return [i[0] for i in mcw_list]

    def loudness(self):
        """Return the loudness"""
        data, rate = sf.read(
            self.output_path)  # load audio (with shape (samples, channels))
        meter = pyln.Meter(rate)  # create BS.1770 meter
        self.loudness = meter.integrated_loudness(data)  # measure loudness

        return self.loudness
