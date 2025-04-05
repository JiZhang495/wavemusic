import tkinter as tk
from tkinter import filedialog, messagebox
from scripts.music import Music
# from playsound import playsound
import re
from scripts.utils import play_wav
from scripts.part_gui import PartGUI
from src.simple import main_pybind

class WaveMusicGUI:
    def __init__(self, root):
        self.frame = tk.Frame(root)

        # text: Hello from wavemusic! Enter your score below:
        label = tk.Label(self.frame, text="Hello from WaveMusic!")
        label.pack(pady=10)
        label.config(font=("Arial", 16))
        instruction_label = tk.Label(self.frame, text="Enter your score below:")
        instruction_label.pack(pady=5)
        instruction_label.config(font=("Arial", 12))

        self.part0 = PartGUI(self)
        self.part1 = PartGUI(self)
        self.part2 = PartGUI(self)
        self.part3 = PartGUI(self)

        # Open file link to load score and save score
        self.file_buttons_frame = tk.Frame(self.frame)
        self.file_buttons_frame.pack(pady=5)

        self.load_file_button = tk.Button(self.file_buttons_frame, text="Load Score", command=self.load_score)
        self.load_file_button.pack(side=tk.LEFT, padx=5)

        self.save_file_button = tk.Button(self.file_buttons_frame, text="Save Score", command=self.save_score)
        self.save_file_button.pack(side=tk.LEFT, padx=5)

        # Frame for filename entries and tickboxes and create WAV button
        self.playmusic_frame = tk.Frame(self.frame)
        self.playmusic_frame.pack(pady=5)

        # Frame for temp file
        self.tempfile_frame = tk.Frame(self.playmusic_frame)
        self.tempfile_frame.pack(side=tk.LEFT, padx=5)
        self.tempfile_frame.config(width=200)
        # textbox for temp file
        tempfile_label = tk.Label(self.tempfile_frame, text="Temp file for live playing: temp.wav")
        tempfile_label.pack(side=tk.TOP, padx=5)
        tempfile_label.config(font=("Arial", 9))
        # tickbox for playing temp file
        self.temp_var = tk.BooleanVar()
        self.temp_var.set(True)  # default to checked
        self.temp_checkbutton = tk.Checkbutton(self.tempfile_frame, text="Live playing with Enter key", variable=self.temp_var)
        self.temp_checkbutton.pack(side=tk.TOP, padx=5)
        self.temp_checkbutton.config(font=("Arial", 9))

        # Frame for full music file
        self.musicfile_frame = tk.Frame(self.playmusic_frame)
        self.musicfile_frame.pack(side=tk.LEFT, padx=5)
        self.musicfile_frame.config(width=200)
        # entry box for filename, default is m.wav, get entry as a variable
        self.filename = tk.StringVar() # save as filename
        self.filename.set("m.wav")
        self.filename_entry = tk.Entry(self.musicfile_frame, textvariable=self.filename, width=20)
        self.filename_entry.pack(side=tk.TOP, padx=5)
        # tickbox for playing WAV
        self.play_var = tk.BooleanVar()
        self.play_var.set(False)  # default to unchecked
        self.play_checkbutton = tk.Checkbutton(self.musicfile_frame, text="Play WAV after creation", variable=self.play_var)
        self.play_checkbutton.pack(side=tk.TOP, padx=5)
        self.play_checkbutton.config(font=("Arial", 9))

        # Button for creating WAV
        self.create_wav_button = tk.Button(self.playmusic_frame, text="Create WAV", 
                                           command=self.create_wav, height=2, width=15)
        # self.create_wav_button = tk.Button(self.playmusic_frame, text="Create WAV", 
        #                                    command=self.create_wav_cpp, height=2, width=15)
        self.create_wav_button.pack(side=tk.LEFT, padx=5)
        self.create_wav_button.config(font=("Arial", 12))

    def load_score(self):
        file_path = filedialog.askopenfilename(
            initialdir="sheets", defaultextension=".wmusic", filetypes=[("WaveMusic Files", "*.wmusic"), ("Text Files", "*.txt")])
        if file_path:
            try:
                self.load_score_filepath(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def load_score_filepath(self, file_path):
        # Clear existing score entries
        self.part0.score_entry.delete(1.0, tk.END)
        self.part1.score_entry.delete(1.0, tk.END)
        self.part2.score_entry.delete(1.0, tk.END)
        self.part3.score_entry.delete(1.0, tk.END)

        with open(file_path) as file:
            score = file.read()
            # # Find all sections starting with a label (e.g. square:, triangle:, etc.)
            # matches = re.findall(r'^(\w+):([\s\S]*?)(?=^\w+:|\Z)', text, re.MULTILINE)
            # # Convert to dictionary: key = label without colon, value = corresponding score
            # score_dict = {label: content.strip() for label, content in matches}
            blocks = re.split(r'(?=\b(?:square|triangle|sine|sawtooth):)', score)
            blocks = [block.strip() for block in blocks if block.strip()]
            if blocks[0]:
                block0 = blocks[0].split(":")
                if len(block0) > 1:
                    self.part0.waveform_var.set(block0[0].strip())
                self.part0.score_entry.insert(tk.END, block0[-1].strip())
            if len(blocks)> 1 and blocks[1]:
                block1 = blocks[1].split(":")
                if len(block1) > 1:
                    self.part1.waveform_var.set(block1[0].strip())
                self.part1.score_entry.insert(tk.END, block1[-1].strip())
            if len(blocks) > 2 and blocks[2]:
                block2 = blocks[2].split(":")
                if len(block2) > 1:
                    self.part2.waveform_var.set(block2[0].strip())
                self.part2.score_entry.insert(tk.END, block2[-1].strip())
            if len(blocks) > 3 and blocks[3]:
                block3 = blocks[3].split(":")
                if len(block3) > 1:
                    self.part3.waveform_var.set(block3[0].strip())
                self.part3.score_entry.insert(tk.END, block3[-1].strip())

    def save_score(self):
        file_path = filedialog.asksaveasfilename(
            initialdir="sheets", defaultextension=".wmusic", filetypes=[("WaveMusic Files", "*.wmusic")])
        if file_path:
            try:
                self.save_score_filepath(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def save_score_filepath(self, file_path):
        with open(file_path, 'w') as file:
            waveform0 = self.part0.waveform_var.get()
            waveform1 = self.part1.waveform_var.get()
            waveform2 = self.part2.waveform_var.get()
            waveform3 = self.part3.waveform_var.get()
            score0 = self.part0.score_entry.get(1.0, tk.END).strip()
            score1 = self.part1.score_entry.get(1.0, tk.END).strip()
            score2 = self.part2.score_entry.get(1.0, tk.END).strip()
            score3 = self.part3.score_entry.get(1.0, tk.END).strip()
            score = (
                f"{waveform0}: {score0} \n"
                f"{waveform1}: {score1} \n"
                f"{waveform2}: {score2} \n"
                f"{waveform3}: {score3}"
            )
            # score = re.sub(r"(\w+):", r"\1:", score)  # remove spaces before colons
            file.write(score)
            return score

    def create_wav(self):
        # score = self.score_entry1.get(1.0, tk.END).strip()
        score = self.save_score_filepath("sheets/temp.wmusic")
        # if not score:
        #     messagebox.showwarning("Warning", "Score is empty!")
        #     return
        if not self.filename.get():
            messagebox.showwarning("Warning", "Filename is empty!")
            return
        filename = self.filename.get()
        if not filename.endswith(".wav"):
            filename += ".wav"
        # if os.path.exists(filename):
        #     overwrite = messagebox.askyesno("Overwrite", f"{filename} already exists. Overwrite?")
        #     if not overwrite:
        #         return
        try:
            # Music(score).write_wav(filename=filename, sample_rate=44100, bpm=100)
            main_pybind(["1", "sheets/temp.wmusic"]) # why need to pass another argument?

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create WAV file: {e}")

        # no need below because C++ implementation already plays the sound
        if self.play_var.get():
            try:
                play_wav(filename=filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to play WAV file: {e}")
            # playsound(filename)

    def create_wav_cpp(self):
        self.save_score_filepath("sheets/temp.wmusic")
        pass # Call the C++ function here to create the WAV file
