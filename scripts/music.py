import wave
import struct
from scripts.note import Note
from scripts.utils import play_wav
ps = None # placeholder for playsound import

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

        with wave.open(filename, "wb") as f:
            f.setnchannels(1)  # mono
            f.setsampwidth(2)  # 2 bytes (16 bits)
            f.setframerate(sample_rate)
            f.writeframes(struct.pack("<" + "h" * len(rawdata), *rawdata))
            # for d in rawdata:
            #     f.writeframesraw(struct.pack("<h", d))
    
    def playscore(self, filename="music.wav", sample_rate=44100, bpm=100):
        self.write_wav(filename=filename, sample_rate=sample_rate, bpm=bpm)
        play_wav(filename=filename)

    def play_from_playsound(self, filename="music.wav", sample_rate=44100, bpm=100):
        """ This method is used to play the music using playsound library after writing WAV.
        """
        global ps
        if ps is None:
            from playsound import playsound
            ps = playsound
        self.write_wav(filename=filename, sample_rate=sample_rate, bpm=bpm)
        ps(filename=filename)
