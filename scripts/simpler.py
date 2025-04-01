#!/usr/bin/env python3
import wave
import struct
import math
import os
from sys import platform
from scripts.utils import (
    is_integer, 
    note_name_to_freq,
)

class note:
    """ "length" is measured as multiples of a semiquaver
    "note" takes either the note name or frequency (Hz) of the note (feature to be added)
    "r" is used as the note name of rests
    """
    def __init__(self, shape="s", length=1, name="r", octave=4):
        self.shape = shape
        self.length = length
        self.name = name
        self.octave = octave
        self.frequency = None 

    def __str__(self):
        return f"{self.length}{self.name}{self.octave}"
    
    def update(self, string):
        # string = string.strip()
        if is_integer(string[0]):
            self.length = int(string[0])
            string = string[1:]
        if is_integer(string[-1]):
            self.octave = int(string[-1])
            string = string[:-1]
        self.name = string
        freq_expt = note_name_to_freq(self.name)
        if freq_expt:
            self.frequency = 440 * math.pow(2, freq_expt / 12 + self.octave - 4)
    
    def update_shape(self, shape):
        if shape in ["q", "s"]:
            self.shape = shape
        else:
            raise ValueError(f"Invalid shape: {shape}. Expected 'q' or 's'.")
        
    def note_to_wave(self, sample_rate, bpm=100):
        semiquaver = 15 / bpm #s
        frames = int(self.length * semiquaver * sample_rate)
        value = []
        if self.frequency == None or self.name == "r":
            for _i in range(frames):
                value.append(0)
        else:
            if self.shape == "s": # sine wave
                for i in range(frames):
                    value.append(int(6000 * math.sin(2 * math.pi * self.frequency * i / sample_rate)))
            elif self.shape == "q": # square wave
                for i in range(frames):
                    if int(float(i) / sample_rate * 2 * self.frequency) % 2:
                        value.append(-2000)
                    else:
                        value.append(2000)
        return value


class music:
    """ This class is used to represent a piece of music.
    It contains a list of notes and a method to play the music.
    """
    def __init__(self, score: str):
        self.score = score.replace("|", "")
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
            note_obj = note(shape=shape)
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


if __name__ == "__main__":
    score = "r 2eb 2f 2g | 2bb 2g 3g r | f f 2eb 3f r | 2eb 2c 2eb 2f | 5g 3r | 2eb " \
    "2c 3eb r | bb3 bb3 2f 3eb r | 2g 2f 2f 2eb | 4f q2eb 2f | 2bb 2g 3g r | f f 2eb 3f r | "\
    "2eb 2c 2eb 2bb | 5g 3r | 2eb 2c 3eb r | bb3 bb3 2f 3eb r | 2g 2f 2eb 2c | 4eb"
    music(score).playscore(filename="music.wav", sample_rate=44100, bpm=100)
