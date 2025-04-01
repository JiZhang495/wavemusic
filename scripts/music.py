import wave
import struct
import os
from sys import platform
from scripts.note import Note
# from playsound import playsound #if play_from_playsound() used

class Music:
    """ This class is used to represent a piece of music.
    It contains a list of notes and a method to play the music.
    """
    def __init__(self, score: str):
        self.score = score.replace("|", "") # remove the bar lines
        self.notes = []
        self.score_to_notes()
    
    def __str__(self):
        return self.score
    
    def score_to_notes(self):
        notelist = self.score.split()
        shape = "s"  # default shape
        for n in notelist:
            n = n.strip()
            if n[0] in ["s", "q"]:
                shape = n[0]
                n = n[1:]
            note_obj = Note(shape=shape)
            note_obj.update(n)
            self.notes.append(note_obj)
    
    def write_wav(self, filename="music.wav", sample_rate=44100, bpm=100): #44100 Hz
        rawdata = []
        for note_obj in self.notes:
            rawdata.extend(note_obj.note_to_wave(sample_rate=sample_rate, bpm=bpm))

        with wave.open(filename, "w") as f:
            f.setnchannels(1) # mono
            f.setsampwidth(2) # 2 bytes (16 bits)
            f.setframerate(sample_rate)
            for d in rawdata:
                f.writeframesraw(struct.pack("<h", d))
    
    def playscore(self, filename="music.wav", sample_rate=44100, bpm=100):
        self.write_wav(filename=filename, sample_rate=sample_rate, bpm=bpm)
        if platform == "linux" or platform == "linux2":
            os.system("aplay " + filename)
        elif platform == "darwin":
            os.system("afplay " + filename)
        elif platform == "win32":
            os.system("start " + filename)
        else:
            print("unsupported platform:" + platform)

    def play_from_playsound(self, filename="music.wav", sample_rate=44100, bpm=100):
        self.write_wav(filename=filename, sample_rate=sample_rate, bpm=bpm)
        # playsound(filename)
