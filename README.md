# WaveMusic
Writing music audio files using sine, square, triangular and sawtooth wave

----

Architecture of the C++ implementation
```



                                                                  main()
                                                             ┌──────────────────────────────────────────────────────────┐
                                                             │                                                          │
                                                             │   Write WAV                                              │
                                                             │   header                                                 │
                                               sigen.cpp     │                                                          │
                                                             │     │                                                    │
┌──────────────────────────────────────────────────────────┐ │     ▼                                                    │
│                                                          │ │                                                          │
│ void play(std::vector<int16_t> &pcm_data,    Generate    │ │   Parse        score_t parse(std::string str_in)         │
│           unsigned int &ptr, shape_t shape,  signals   ◄─┼─┼── score                                                  │
│           unsigned int length, float freq,               │ │                                                          │
│           bool first)                           │        │ │     │                                                    │
│                                                 ▼        │ │     │                                                    │
│                                                          │ │     │                                                    │
│ float filter(unsigned int i,                 A/R filter  │ │     │                                                    │
│              unsigned int s_len)                         │ │     │                                                    │
│                                                 │        │ │     │                                                    │
│                                                 ▼        │ │     ▼                                                    │
│                                                          │ │                                                          │
│ std::vector<int16_t>                         Low pass  ──┼─┼─► Write        void play(std::vector<int16_t> &pcm_data, │
│   lowpass(std::vector<int16_t> &pcm_data)    filter      │ │   notes                  unsigned int &ptr, note_t note, │
│                                                          │ │                          bool first);                    │
└──────────────────────────────────────────────────────────┘ │     │                                                    │
                                                             │     ▼                                                    │
                                                             │                                                          │
                                                             │   Fill in data size                                      │
                                                             │   WAV header                                             │
                                                             │                                                          │
                                                             │     │                                                    │
                                                             │     ▼                                                    │
                                                             │                                                          │
                                                             │   Playback                                               │
                                                             │   with                                                   │
                                                             │   system Call                                            │
                                                             │                                                          │
                                                             └──────────────────────────────────────────────────────────┘
```

----
To use the C++ version:
```bash
make simple
```
```bash
./simple src/<title>.wmusic
```

for debug mode:
```bash
make refresh DEBUG=1
```
```bash
./simple src/<title>.wmusic
```

----
The *wave* module in the Python standard library provides a convenient interface to the WAV sound format.
References:
<https://docs.python.org/3/library/wave.html>
<https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave>

We can write some music with this module. We also intend to write music from waves with C++.

----
The *playsound* module can be used to play the WAV file generated. Run the following command to install it:
```bash
pip install playsound==1.2.2
```

Then to run the python script:
```bash
./simplest.py
```

----
The *simplest.py* script in the *src* folder demonstrates creation of simple monophonic melodies with sine waves and square waves.
The song is "Ting Wo Shuo Xie Xie Ni".
We would like to add more features to the program to produce chords and more complicated melodies in the future.
The *simpler.py* script is an alternative version of *simplest.py*, and *simple.cpp* demonstrates a way of doing it in C++.

----

TODO list:

 - [x] consistent note length
 - [ ] functional REPL
 - [x] triangle wave generation
 - [x] polyphony doesn't sound out of tune anymore?
 - [x] saw and square waves sounds bad, add LPF to soften it
