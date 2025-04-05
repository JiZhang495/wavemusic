
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


### On Linux

(Note: WSL may need extra configuration to display GUI and play sound.)

To incorporate the C++ code as a backend, use pybind11:
```bash
sudo apt install python3-dev g++ cmake pybind11-dev
```
```bash
uv run setup.py build_ext --inplace
```
where [uv](https://docs.astral.sh/uv/) is recommended for dependency management.

To run the python script:
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

To build a standalone app:
```bash
uv run pyinstaller main.py --onefile 
# pyinstaller main.py --onefile --clean --noconsole --icon=icon.ico
```


### On Windows

Use [MSYS2](https://www.msys2.org/) MINGW x64 terminal:
```bash
pacman -Syu
# Close terminal, reopen it (again in MinGW 64-bit)
pacman -Syu
```
To use inside VScode: In VScode, open Settings, search for 'terminal.integrated.profiles.windows' - Edit in settings.json - add:
```json
"terminal.integrated.profiles.windows": {
  "MSYS2 MinGW 64-bit": {
    "path": "C:\\msys64\\usr\\bin\\bash.exe",
    "args": ["--login", "-i"],
    "env": {
      "MSYSTEM": "MINGW64",
      "CHERE_INVOKING": "1"
    }
  }
},
"terminal.integrated.defaultProfile.windows": "MSYS2 MinGW 64-bit"
```
Restart VScode, open terminal.
```bash
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-cmake mingw-w64-x86_64-python-pip mingw-w64-x86_64-pybind11 git
g++ --version
python --version
cmake --version
```
Set up .venv and dependencies (uv can be tricky in MSYS2 Mingw)
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```
```bash
python setup.py build_ext --inplace
```
To run the python script:
```bash
python main.py
```
To build a standalone app:
```bash
pyinstaller main.py --onefile 
# pyinstaller main.py --onefile --clean --noconsole --icon=icon.ico
```


----
Python TODO list:

 - [x] use C++ code as a backend
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
