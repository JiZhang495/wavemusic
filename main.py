#!/usr/bin/env python3
from scripts.music import Music
import tkinter as tk
from scripts.gui import WaveMusicGUI

def main():
    print("Hello from wavemusic!")
    score = "s1r 2eb 2f 2g | 2bb 2g 3g 1r | 1f 1f 2eb 3f 1r | 2eb 2c 2eb 2f | 5g 3r | t2eb " \
    "2c 3eb 1r | 1bb3 1bb3 2f 3eb 1r | 2g 2f 2f 2eb | 4f q2eb 2f | 2bb 2g 3g 1r | 1f 1f 2eb 3f 1r | "\
    "2eb 2c 2eb 2bb | 5g 3r | w2eb 2c 3eb 1r | 1bb3 1bb3 2f 3eb 1r | 2g 2f 2eb 2c | 4eb"
    Music(score).playscore(filename="music.wav", sample_rate=44100, bpm=100)

def main_gui():
    root = tk.Tk()
    app = WaveMusicGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # main()
    main_gui()
