#!/usr/bin/env python3

import wave, struct, math, os
from sys import platform

def play(sampleRate, length, note, octave=4, shape='q'):
    ''' "length" is measured as multiples of a semiquaver
        the argument "note" takes either the note name or frequency (Hz) of the note
    '''
    BPM = 100
    semiquaver = 15/BPM #s

    A, As, B, C, Cs, D, Ds, E, F, Fs, G, Gs = \
            [55 * math.pow(2,(i/12)) for i in range(12)] #Hz
    A *= 2
    As *= 2
    B *= 2
    # represent frequencies at 2nd octave
    freq = {'A': A, 'As': As, 'Bb': As, 'B': B, 'C': C, 'Cs': Cs, \
            'Db': Cs, 'D': D, 'Ds': Ds, 'Eb': Ds, 'E': E, 'F': F, \
            'Fs': Fs, 'Gb': Fs, 'G': G, 'Gs': Gs, 'Ab': Gs, 'X': 0}

    if type(note) == str:
        note = freq[note] * math.pow(2,(octave-2)) #pitch
    frames = int(length * semiquaver * sampleRate)
    value = []
    if note != 0:
        if shape == 'q': #square wave
            for i in range(frames):
                if int(float(i)/sampleRate*2*note)%2 == 0:
                    value.append(2000)
                else:
                    value.append(-2000)

        elif shape == 's': #sine wave
            for i in range(frames):
                value.append(int(6000 * math.sin(2 * math.pi * note * i/sampleRate)))
    else:
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
    sampleRate = 44100 #Hz
    file.setframerate(sampleRate)

    rawdata = []
    # Writing a monophonic melody
    rawdata.extend(play(sampleRate, 1, 'X'))
    rawdata.extend(play(sampleRate, 2, 'Eb',4, 's'))
    rawdata.extend(play(sampleRate, 2, 'F',4, 's'))
    rawdata.extend(play(sampleRate, 2, 'G',4, 's'))
    rawdata.extend(play(sampleRate, 2, 'Bb',4, 's'))
    rawdata.extend(play(sampleRate, 2, 'G',4, 's'))
    rawdata.extend(play(sampleRate, 3, 'G',4, 's'))
    rawdata.extend(play(sampleRate, 1, 'X'))
    rawdata.extend(play(sampleRate, 1, 'F',4, 's'))
    rawdata.extend(play(sampleRate, 1, 'F',4, 's'))
    rawdata.extend(play(sampleRate, 2, 'Eb',4, 's'))
    rawdata.extend(play(sampleRate, 3, 'F',4, 's'))
    rawdata.extend(play(sampleRate, 1, 'X'))

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
