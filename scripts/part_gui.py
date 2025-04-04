import tkinter as tk
from tkinter import messagebox
from scripts.music import Music
from scripts.utils import play_wav

class PartGUI:
    def __init__(self, master):
        self.master = master
        self.part_frame = tk.Frame(master.frame)
        self.part_frame.pack(pady=5)

        # Part options
        self.options_frame = tk.Frame(self.part_frame)
        self.options_frame.pack(side=tk.LEFT, padx=5)
        self.options_frame.config(width=300)

        self.waveform_label = tk.Label(self.options_frame, text="Waveform:")
        self.waveform_label.pack(side=tk.TOP, padx=0)
        self.waveform_label.config(font=("Arial", 9))
        self.waveform_var = tk.StringVar()
        self.waveform_var.set("triangle")  # default to triangle
        self.waveform_menu = tk.OptionMenu(self.options_frame, self.waveform_var, "triangle", "sine", "square", "sawtooth")
        self.waveform_menu.pack(side=tk.TOP, padx=5)
        self.waveform_menu.config(font=("Arial", 9))

        # Part score entry
        self.score_entry = tk.Text(self.part_frame, width=100, height=6)
        self.score_entry.pack(side=tk.LEFT, padx=5)
        self.score_entry.config(font=("Courier", 10))
        # Plays previous line upon pressing Enter
        self.score_entry.bind("<Return>", lambda _: self.play_line())

    def play_line(self):
        # Get last line of text in score_entry and write to temp.wav
        if not self.master.temp_var:
            return
        score = self.score_entry.get("1.0", tk.END).strip()
        if not score:
            return
        last_line = score.splitlines()[-1].strip()
        if not last_line:
            return
        try:
            # insert the waveform type at the beginning of the line
            last_line = f"{self.waveform_var.get()}: {last_line}"
            Music(last_line).write_wav(filename="temp.wav", sample_rate=44100, bpm=100)
            play_wav("temp.wav")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play line: {e}")
