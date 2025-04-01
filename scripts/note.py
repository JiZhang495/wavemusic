import math
from scripts.utils import (
    is_integer, 
    note_name_to_freq,
)

class Note:
    """ "length" is measured as multiples of a semiquaver
    "note" takes either the note name or frequency (Hz) of the note (feature to be added)
    "r" is used as the note name of rests
    """
    def __init__(self, shape="s", length=2, name="r", octave=4):
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
        if self.frequency is None or self.name == "r":
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
