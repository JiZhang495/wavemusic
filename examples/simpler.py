#!/usr/bin/env python3

import wave, struct, math, os
from sys import platform

def play(sampleRate, length, note, octave=4, shape='q'):
    ''' "length" is measured as multiples of a semiquaver
        "note" takes either the note name or frequency (Hz) of the note
        "X" is used as the note name of rests
    '''
    BPM = 100
    semiquaver = 15/BPM #s

    freq = {'C': -9, 'Cs': -8, 'Db': -8, 'D': -7, 'Ds': -6, 'Eb': -6, 'E': -5,
            'F': -4, 'Fs': -3, 'Gb': -3, 'G': -2, 'Gs': -1, 'Ab': -1, 'A': 0,
            'As': 1, 'Bb': 1, 'B': 2}

    frames = int(length * semiquaver * sampleRate)
    value = []
    if note == 'X' or note == 0:
        for i in range(frames):
            value.append(0)

    else:
        if type(note) == str:
            note = 440 * math.pow(2, freq[note]/12 + octave - 4) #pitch

        if shape == 'q': #square wave
            for i in range(frames):
                if int(float(i)/sampleRate*2*note)%2:
                    value.append(2000)
                else:
                    value.append(-2000)

        elif shape == 's': #sine wave
            for i in range(frames):
                value.append(int(6000*math.sin(2*math.pi*note*i/sampleRate)))

    return value

def write(file, value):
    for d in value:
        data = struct.pack('<h', d)
        file.writeframesraw(data)


def main():
    filename = 'music.wav'
    file = wave.open(filename, 'w')
    file.setnchannels(1) #mono
    file.setsampwidth(2)
    sampleRate = 44100 #Hz
    file.setframerate(sampleRate)

    score = [ [1, 'X'],
            [2, 'Eb', 4, 's'],
            [2, 'F',  4, 's'],
            [2, 'G',  4, 's'],
            [2, 'Bb', 4, 's'],
            [2, 'G',  4, 's'],
            [3, 'G',  4, 's'],
            [1, 'X'],
            [1, 'F',  4, 's'],
            [1, 'F',  4, 's'],
            [2, 'Eb', 4, 's'],
            [3, 'F',  4, 's'],
            [1, 'X'],
            [2, 'Eb', 4, 's'],
            [2, 'C',  4, 's'],
            [2, 'Eb', 4, 's'],
            [2, 'F',  4, 's'],
            [5, 'G',  4, 's'],
            [3, 'X'],
            [2, 'Eb', 4, 's'],
            [2, 'C',  4, 's'],
            [3, 'Eb', 4, 's'],
            [1, 'X'],
            [1, 'Bb', 3, 's'],
            [1, 'Bb', 3, 's'],
            [2, 'F',  4, 's'],
            [3, 'Eb', 4, 's'],
            [1, 'X'],
            [2, 'G',  4, 's'],
            [2, 'F',  4, 's'],
            [2, 'F',  4, 's'],
            [2, 'Eb', 4, 's'],
            [4, 'F',  4, 's'],
            [2, 'Eb'],
            [2, 'F'],
            [2, 'Bb'],
            [2, 'G'],
            [3, 'G'],
            [1, 'X'],
            [1, 'F'],
            [1, 'F'],
            [2, 'Eb'],
            [3, 'F'],
            [1, 'X'],
            [2, 'Eb'],
            [2, 'C'],
            [2, 'Eb'],
            [2, 'Bb'],
            [5, 'G'],
            [3, 'X'],
            [2, 'Eb'],
            [2, 'C'],
            [3, 'Eb'],
            [1, 'X'],
            [1, 'Bb', 3],
            [1, 'Bb', 3],
            [2, 'F'],
            [3, 'Eb'],
            [1, 'X'],
            [2, 'G'],
            [2, 'F'],
            [2, 'Eb'],
            [2, 'C'],
            [4, 'Eb'] ]

    # Writing a monophonic melody
    rawdata = []
    for note in score:
        rawdata.extend(play(sampleRate, *note))

    write(file, rawdata)

    file.close()

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
