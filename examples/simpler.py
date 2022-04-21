#!/usr/bin/env python3

import wave, struct, math, os
from sys import platform

# TODO: global variables bad
sampleRate = 44100.0 #Hz
BPM = 100.0
semiquaver = 15.0/BPM #s

def play(length, note, octave=4, shape='q'): # "length" is measured as multiples of a semiquaver
                  # the argument "note" takes either the note name or frequency (Hz) of the note

    A, As, B, C, Cs, D, Ds, E, F, Fs, G, Gs = \
            [55.00 * math.pow(2,(i/12)) for i in range(12)] #Hz
    A *= 2
    As *= 2
    B *= 2
    # represent frequencies at 2nd octave
    freq = {'A': A, 'As': As, 'Bb': As, 'B': B, 'C': C, 'Cs': Cs, \
            'Db': Cs, 'D': D, 'Ds': Ds, 'Eb': Ds, 'E': E, 'F': F, \
            'Fs': Fs, 'Gb': Fs, 'G': G, 'Gs': Gs, 'Ab': Gs}

    if type(note) == str:
        note = freq[note] * math.pow(2,(octave-2)) #pitch
    frames = int(length * semiquaver * sampleRate)
    value = []
    if shape == 'q': #square wave
        for i in range(frames):
            if int(float(i)/sampleRate*2*note)%2 == 0:
                value.append(2000)
            else:
                value.append(-2000)

    elif shape == 's': #sine wave
        for i in range(frames):
            value.append(int(6000 * math.sin(2 * math.pi * note * float(i)/sampleRate)))

    return value

def rest(length):
    frames = int(length * semiquaver * sampleRate)
    value = []
    for i in range(frames):
        value.append(0)
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
    file.setframerate(sampleRate)

    # Writing a monophonic melody
    write(file, rest(1))
    write(file, play(2, 'Eb',4, 's'))
    write(file, play(2, 'F',4, 's'))
    write(file, play(2, 'G',4, 's'))
    write(file, play(2, 'Bb',4, 's'))
    write(file, play(2, 'G',4, 's'))
    write(file, play(3, 'G',4, 's'))
    write(file, rest(1))
    write(file, play(1, 'F',4, 's'))
    write(file, play(1, 'F',4, 's'))
    write(file, play(2, 'Eb',4, 's'))
    write(file, play(3, 'F',4, 's'))
    write(file, rest(1))

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