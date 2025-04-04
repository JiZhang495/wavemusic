#!/usr/bin/env python3
from scripts.music import Music
import tkinter as tk
import sys
from scripts.gui import WaveMusicGUI
from scripts.music import Music

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WaveMusic")
        self.gui = WaveMusicGUI(root)
        self.gui.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def main_gui():
    try:
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error running tkinter: {e}")
        root.destroy()
        print("Starting in CLI mode...")
        main()

def main(*args):
    # Command line interface for playing music
    print("Hello from wavemusic!")
    if args[0] == "gui":
        main_gui()
        return
    if args[0] == "cli":
        pass
    else:
        try:
            score_file = args[0].replace(" ", "").replace("\n", "").replace("\r", "")
            with open(score_file, "r") as f:
                score = f.read()
            print(f"Score loaded from {score_file}")
        except FileNotFoundError:
            print(f"File {score_file} not found. Using default score.")
            score = "s1r 2eb 2f 2g | 2bb 2g 3g 1r | 1f 1f 2eb 3f 1r | 2eb 2c 2eb 2f | 5g 3r | t2eb " \
                    "2c 3eb 1r | 1bb3 1bb3 2f4 3eb 1r | 2g 2f 2f 2eb | 4f q2eb 2f | 2bb 2g 3g 1r | 1f 1f 2eb 3f 1r | "\
                    "2eb 2c 2eb 2bb | 5g 3r | w2eb 2c 3eb 1r | 1bb3 1bb3 2f4 3eb 1r | 2g 2f 2eb 2c | 4eb"
        print(score)
        try:
            Music(score).playscore(filename="m.wav", sample_rate=44100, bpm=100)
            print("Playing score...")
            return
        except Exception as e:
            print(f"Error playing score: {e}")
            return

    score = input("Enter your score (enter :q to finish entry): ")
    if score == ":q":
        print("No score entered. Exiting...")
        return
    Music(score).playscore(filename="temp.wav", sample_rate=44100, bpm=100)
    input_score = ""
    while input_score != ":q":
        score += input_score + " "
        input_score = input()
        Music(input_score).playscore(filename="temp.wav", sample_rate=44100, bpm=100)
    score = score.replace("|", "")  # remove the bar lines
    if score is None or score == "":
        print("No score entered. Exiting...")
        return
    try:
        Music(score).playscore(filename="m.wav", sample_rate=44100, bpm=100)
        print("Playing score...")
    except Exception as e:
        print(f"Error playing score: {e}")
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(*sys.argv[1:])
    else:
        main_gui()
