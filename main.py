#!/usr/bin/env python3
from scripts.simpler import music

def main():
    print("Hello from wavemusic!")
    score = "r 2eb 2f 2g | 2bb 2g 3g r | f f 2eb 3f r | 2eb 2c 2eb 2f | 5g 3r | 2eb " \
    "2c 3eb r | bb3 bb3 2f 3eb r | 2g 2f 2f 2eb | 4f q2eb 2f | 2bb 2g 3g r | f f 2eb 3f r | "\
    "2eb 2c 2eb 2bb | 5g 3r | 2eb 2c 3eb r | bb3 bb3 2f 3eb r | 2g 2f 2eb 2c | 4eb"
    music(score).playscore(filename="music.wav", sample_rate=44100, bpm=100)

if __name__ == "__main__":
    main()
