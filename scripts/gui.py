import tkinter as tk
from tkinter import filedialog, messagebox
from scripts.music import Music
from playsound import playsound
from scripts.utils import play_wav

class WaveMusicGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WaveMusic")

        # text: Hello from wavemusic! Enter your score below:
        self.label = tk.Label(root, text="Hello from WaveMusic!")
        self.label.pack(pady=10)
        self.label.config(font=("Arial", 16))
        self.instruction_label = tk.Label(root, text="Enter your score below:")
        self.instruction_label.pack(pady=5)
        self.instruction_label.config(font=("Arial", 12))

        # Entry box for typing score
        self.score_entry = tk.Text(root, height=15, width=80)
        self.score_entry.pack(pady=10)
        self.score_entry.config(font=("Courier", 10))
        # example score
        example_score = "s1r eb f g | bb g 3g 1r | 1f 1f eb 3f 1r | eb c eb f | 5g 3r | teb " \
        "c 3eb 1r | 1bb3 1bb3 f 3eb 1r | g f f eb | 4f qeb f | bb g 3g 1r | 1f 1f eb 3f 1r | "\
        "eb c eb bb | 5g 3r | web c 3eb 1r | 1bb3 1bb3 f 3eb 1r | g f eb c | 4eb"
        self.score_entry.insert(tk.END, example_score)

        # Plays previous line upon pressing Enter
        self.score_entry.bind("<Return>", lambda _: self.play_line())

        # Open file link to load score and save score
        self.file_buttons_frame = tk.Frame(root)
        self.file_buttons_frame.pack(pady=5)

        self.open_file_button = tk.Button(self.file_buttons_frame, text="Load Score", command=self.load_score)
        self.open_file_button.pack(side=tk.LEFT, padx=5)

        self.save_file_button = tk.Button(self.file_buttons_frame, text="Save Score", command=self.save_score)
        self.save_file_button.pack(side=tk.LEFT, padx=5)

        # Frame for filename entries and tickboxes and create WAV button
        self.playmusic_frame = tk.Frame(root)
        self.playmusic_frame.pack(pady=5)

        # Frame for temp file
        self.tempfile_frame = tk.Frame(self.playmusic_frame)
        self.tempfile_frame.pack(side=tk.LEFT, padx=5)
        self.tempfile_frame.config(width=200)

        # textbox for temp file
        self.tempfile_label = tk.Label(self.tempfile_frame, text="Temp file for live playing: temp.wav")
        self.tempfile_label.pack(side=tk.TOP, padx=5)
        self.tempfile_label.config(font=("Arial", 9))

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

        # entry box for filename, default is music.wav, get entry as a variable
        self.filename = tk.StringVar()
        self.filename.set("music.wav")
        self.filename_entry = tk.Entry(self.musicfile_frame, textvariable=self.filename, width=20)
        self.filename_entry.pack(side=tk.TOP, padx=5)

        # tickbox for playing WAV
        self.play_var = tk.BooleanVar()
        self.play_var.set(True)  # default to checked
        self.play_checkbutton = tk.Checkbutton(self.musicfile_frame, text="Play WAV after creation", variable=self.play_var)
        self.play_checkbutton.pack(side=tk.TOP, padx=5)
        self.play_checkbutton.config(font=("Arial", 9))

        # Button for creating WAV
        self.create_wav_button = tk.Button(self.playmusic_frame, text="Create WAV", command=self.create_wav, height=2, width=15)
        self.create_wav_button.pack(side=tk.LEFT, padx=5)
        self.create_wav_button.config(font=("Arial", 12))

    def load_score(self):
        file_path = filedialog.askopenfilename(
            initialdir="sheets", defaultextension=".txt", filetypes=[("WaveMusic Files", "*.wmusic"), ("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path) as file:
                    score = file.read()
                    self.score_entry.delete(1.0, tk.END)
                    self.score_entry.insert(tk.END, score)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")#
    
    def save_score(self):
        file_path = filedialog.asksaveasfilename(
            initialdir="sheets", defaultextension=".txt", filetypes=[("WaveMusic Files", "*.wmusic")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    score = self.score_entry.get(1.0, tk.END).strip()
                    file.write(score)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def create_wav(self):
        score = self.score_entry.get(1.0, tk.END).strip()
        if not score:
            messagebox.showwarning("Warning", "Score is empty!")
            return
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
            Music(score).write_wav(filename=filename, sample_rate=44100, bpm=100)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create WAV file: {e}")
        if self.play_var.get():
            try:
                play_wav(filename=filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to play WAV file: {e}")
            # playsound(filename)
    
    def play_line(self):
        # get last line of text in score_entry and write to temp.wav
        score = self.score_entry.get(1.0, tk.END).strip()
        if not score:
            return
        last_line = score.splitlines()[-1]  # Extract the last line
        if not last_line.strip():  # Check if the last line is empty
            return
        try:
            Music(last_line).write_wav(filename="temp.wav", sample_rate=44100, bpm=100)
            play_wav(filename="temp.wav")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play line: {e}")

        