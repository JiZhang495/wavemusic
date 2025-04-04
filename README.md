
# WaveMusic
Writing music audio files using sine, square, triangular and sawtooth wave


## C++ Implementation

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


## Python Implementation

The *wave* module in the Python standard library provides a convenient interface to the WAV sound format.
References:
<https://docs.python.org/3/library/wave.html>
<https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave>

The demo song is "Ting Wo Shuo Xie Xie Ni".
We would like to add more features to the program to produce chords and more complicated melodies in the future.


To run the python script:
```bash
./main.py
```

With uv:
```bash
uv run main.py
```
or
```bash
uv run main.py gui
```
To use command-line interface:
```bash
uv run main.py cli
```
To generate WAV from score:
```bash
uv run main.py sheets/<title>.wmusic
```


----
Python TODO list:

 - [ ] use C++ code as a backend
 - [x] add waveforms.py to store functions for each waveform
 - [ ] use () to pass frequecies or chords
 - [ ] add bpm and sample rate selection
 - [ ] use numpy for faster performance
 - [ ] the functions can be added to produce complex timber and polyphony
 - [ ] add loudness: ff, f, fp, p, pp
 - [ ] add dynamics: cresc, dim
 - [ ] add timber
 - [x] GUI
 - [ ] add polyphony (fugue)
 - [ ] live waveform plotting matplotlib like oscilloscope
 - [x] playsound on the go with Enter (plays the line just completed)
 - [ ] threading, running playsound at background (already okay with vlc open)

C++ TODO list:

 - [x] consistent note length
 - [ ] functional REPL
 - [x] triangle wave generation
 - [x] polyphony doesn't sound out of tune anymore?
 - [x] saw and square waves sounds bad, add LPF to soften it


----
Using [uv](https://docs.astral.sh/uv/) for Python dependency management

Installing uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Syncing Python version, .venv, dependencies (optional command):
```bash
uv sync
```
Using .venv (optional command, as it should be automatic):
```bash
source ./venv/Scripts/activate
```
Syncing and running project:
```bash
uv run main.py
```
Linting with ruff:
```bash
uvx ruff check .
```
```bash
uvx ruff format
```

Other useful commands:

Creating 'pyproject.toml' and '.python-version:
```bash
uv init
```
Adding package dependencies to 'pyproject.toml':
```bash
uv add <package>
```
Adding package dependencies from 'requirements.txt' to 'pyproject.toml':
```bash
uv add -r requirements.txt
```
Adding ruff and pytest as development dependencies:
```bash
uv add ruff --dev
```
```bash
uv add pytest --dev
```
Generating 'requirements.txt' from a UV lock file:
```bash
uv export -o requirements.txt
```
