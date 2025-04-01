# WaveMusic
Writing music audio files using sine, square, triangular and sawtooth wave

----

Architecture of the C++ implementation
```



                                  main()
                             ┌──────────────────────────┐
                             │                          │
                             │   Write WAV              │
                             │   header                 │
               sigen.cpp     │                          │
                             │     │                    │
┌──────────────────────────┐ │     ▼                    │
│                          │ │                          │
│ play()       Generate    │ │   Parse        parse()   │
│              signals   ◄─┼─┼── score                  │
│                          │ │                          │
│                 │        │ │     │                    │
│                 ▼        │ │     │                    │
│                          │ │     │                    │
│ filter()     A/R filter  │ │     │                    │
│                          │ │     │                    │
│                 │        │ │     │                    │
│                 ▼        │ │     ▼                    │
│                          │ │                          │
│ lowpass()    Low pass  ──┼─┼─► Write                  │
│              filter      │ │   notes                  │
│                          │ │                          │
└──────────────────────────┘ │     │                    │
                             │     ▼                    │
                             │                          │
                             │   Insert data size       │
                             │   in WAV header          │
                             │                          │
                             │     │                    │
                             │     ▼                    │
                             │                          │
                             │   Playback               │
                             │   with                   │
                             │   system Call            │
                             │                          │
                             └──────────────────────────┘
```

----
To use the C++ version:
```bash
make simple
```
```bash
./simple sheets/<title>.wmusic
```

for debug mode:
```bash
make refresh DEBUG=1
```
```bash
./simple sheets/<title>.wmusic
```

----
The *wave* module in the Python standard library provides a convenient interface to the WAV sound format.
References:
<https://docs.python.org/3/library/wave.html>
<https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave>

----
The *playsound* module can be used to play the WAV file generated. Run the following command to install it:
```bash
pip install playsound==1.2.2
```

Then to run the python script:
```bash
./main.py
```

----
The demo song is "Ting Wo Shuo Xie Xie Ni".
We would like to add more features to the program to produce chords and more complicated melodies in the future.

----
Python TODO list:
 - [ ] add waveforms.py to store functions for each waveform
 - [ ] the functions can be added to produce complex timber and polyphony
 - [ ] add loudness: ff, f, fp, p, pp
 - [ ] add dynamics: cresc, dim
 - [ ] add timber
 - [ ] GUI
 - [ ] add polyphony (fugue)

C++ TODO list:

 - [x] consistent note length
 - [ ] functional REPL
 - [x] triangle wave generation
 - [x] polyphony doesn't sound out of tune anymore?
 - [x] saw and square waves sounds bad, add LPF to soften it

