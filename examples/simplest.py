"""
Written by JiZhang495 on 21 Apr 2022
"""

import wave, struct, math, time
from playsound import playsound

sampleRate = 44100.0 #Hz
filename = 'music.wav'
# If a path is included with the file name, make sure to use foward slash '/'

BPM = 100.0
semiquaver = 15.0/BPM #s

A, As, B, C, Cs, D, Ds, E, F, Fs, G, Gs = \
        [55.00 * math.pow(2,(i/12)) for i in range(12)] #Hz
A *= 2
As *= 2
B *= 2
# represent frequencies at 2nd octave
freq = {'A': A, 'As': As, 'Bb': As, 'B': B, 'C': C, 'Cs': Cs, \
        'Db': Cs, 'D': D, 'Ds': Ds, 'Eb': Ds, 'E': E, 'F': F, \
        'Fs': Fs, 'Gb': Fs, 'G': G, 'Gs': Gs, 'Ab': Gs}

file = wave.open(filename, 'w')
file.setnchannels(1) #mono
file.setsampwidth(2)
file.setframerate(sampleRate)

def play(length, note, octave=4, shape='q'): # "length" is measured as multiples of a semiquaver
                  # the argument "note" takes either the note name or frequency (Hz) of the note
    if type(note) == str:
        note = freq[note] * math.pow(2,(octave-2)) #pitch
    frames = int(length * semiquaver * sampleRate)
    if shape == 'q': #square wave
        for i in range(frames):
            if int(float(i)/sampleRate*2*note)%2 == 0:
                value = 2000
            else:
                value = -2000
            data = struct.pack('<h', value)
            file.writeframesraw(data)
    elif shape == 's': #sine wave
        for i in range(frames):
            value = int(6000 * math.sin(2 * math.pi * note * \
                    float(i)/sampleRate))
            data = struct.pack('<h', value)
            file.writeframesraw(data)

def rest(length):
    frames = int(length * semiquaver * sampleRate)
    for i in range(frames):
        data = struct.pack('<h', 0)
        file.writeframesraw(data)

# Writing a monophonic melody
rest(1)
play(2, 'Eb',4, 's')
play(2, 'F',4, 's')
play(2, 'G',4, 's')
play(2, 'Bb',4, 's')
play(2, 'G',4, 's')
play(3, 'G',4, 's')
rest(1)
play(1, 'F',4, 's')
play(1, 'F',4, 's')
play(2, 'Eb',4, 's')
play(3, 'F',4, 's')
rest(1)
play(2, 'Eb',4, 's')
play(2, 'C',4, 's')
play(2, 'Eb',4, 's')
play(2, 'F',4, 's')
play(5, 'G',4, 's')
rest(3)
play(2, 'Eb',4, 's')
play(2, 'C',4, 's')
play(3, 'Eb',4, 's')
rest(1)
play(1, 'Bb',3, 's')
play(1, 'Bb',3, 's')
play(2, 'F',4, 's')
play(3, 'Eb',4, 's')
rest(1)
play(2, 'G',4, 's')
play(2, 'F',4, 's')
play(2, 'F',4, 's')
play(2, 'Eb',4, 's')
play(4, 'F',4, 's')

play(2, 'Eb')
play(2, 'F')
play(2, 'Bb')
play(2, 'G')
play(3, 'G')
rest(1)
play(1, 'F')
play(1, 'F')
play(2, 'Eb')
play(3, 'F')
rest(1)
play(2, 'Eb')
play(2, 'C')
play(2, 'Eb')
play(2, 'Bb')
play(5, 'G')
rest(3)
play(2, 'Eb')
play(2, 'C')
play(3, 'Eb')
rest(1)
play(1, 'Bb',3)
play(1, 'Bb',3)
play(2, 'F')
play(3, 'Eb')
rest(1)
play(2, 'G')
play(2, 'F')
play(2, 'Eb')
play(2, 'C')
play(4, 'Eb')


file.close()
time.sleep(0.1)
playsound(filename) # play the WAV file written

