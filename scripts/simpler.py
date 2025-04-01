#!/usr/bin/env python3

import wave, struct, math, os
from sys import platform


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def note_name_to_freq(name):
    map = {
        "c": -9,
        "cs": -8,
        "db": -8,
        "d": -7,
        "ds": -6,
        "eb": -6,
        "e": -5,
        "f": -4,
        "fs": -3,
        "gb": -3,
        "g": -2,
        "gs": -1,
        "ab": -1,
        "a": 0,
        "as": 1,
        "bb": 1,
        "b": 2,
    }
    return map.get(name.lower(), None) # case insensitive, returns None if not found

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

def score_to_notes(score: str):
    notelist = score.split()
    notes = []
    shape = "s"  # default shape
    for n in notelist:
        n = n.strip()
        if n[0] in ["s", "q"]:
            shape = n[0]
            n = n[1:]
        note_obj = note(shape=shape)
        note_obj.update(n)
        notes.append(note_obj)
    return notes

def write(file, value):
    for d in value:
        data = struct.pack("<h", d)
        file.writeframesraw(data)

def main():
    score = "r 2eb4 2f4 2g4 2bb4 2g4 3g4 r f4 f4 2eb4 3f4 r 2eb4 2c4 2eb4 2f4 5g4 3r 2eb4 " \
    "2c4 3eb4 r bb3 bb3 2f4 3eb4 r 2g4 2f4 2f4 2eb4 4f4 q2eb 2f 2bb 2g 3g r f f 2eb 3f r "\
    "2eb 2c 2eb 2bb 5g 3r 2eb 2c 3eb r bb3 bb3 2f 3eb r 2g 2f 2eb 2c 4eb"

    notes = score_to_notes(score)
    
    # Writing a monophonic melody
    rawdata = []
    sample_rate = 44100  # Hz
    for note_obj in notes:
        rawdata.extend(note_obj.note_to_wave(sample_rate))

    filename = "music.wav"
    with wave.open(filename, "w") as f:
        f.setnchannels(1)  # mono
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        write(f, rawdata)

    if platform == "linux" or platform == "linux2":
        os.system("aplay " + filename)
    elif platform == "darwin":
        os.system("afplay " + filename)
    elif platform == "win32":
        os.system("start " + filename)
    else:
        print("unsupported platform:" + platform)


if __name__ == "__main__":
    main()
