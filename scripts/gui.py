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
        self.score_entry = tk.Text(root, height=15, width=50)
        self.score_entry.pack(pady=10)
        self.score_entry.config(font=("Courier", 10))
        # example score
        example_score = "r 2eb 2f 2g | 2bb 2g 3g r | f f 2eb 3f r | 2eb 2c 2eb 2f | 5g 3r | 2eb " \
        "2c 3eb r | bb3 bb3 2f 3eb r | 2g 2f 2f 2eb | 4f q2eb 2f | 2bb 2g 3g r | f f 2eb 3f r | "\
        "2eb 2c 2eb 2bb | 5g 3r | 2eb 2c 3eb r | bb3 bb3 2f 3eb r | 2g 2f 2eb 2c | 4eb"
        self.score_entry.insert(tk.END, example_score)

        # Open file link to load score and save score
        self.file_buttons_frame = tk.Frame(root)
        self.file_buttons_frame.pack(pady=5)

        self.open_file_button = tk.Button(self.file_buttons_frame, text="Load Score", command=self.load_score)
        self.open_file_button.pack(side=tk.LEFT, padx=5)

        self.save_file_button = tk.Button(self.file_buttons_frame, text="Save Score", command=self.save_score)
        self.save_file_button.pack(side=tk.LEFT, padx=5)

        # Frame for filename entry and tickbox
        self.playmusic_frame = tk.Frame(root)
        self.playmusic_frame.pack(pady=5)

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
            initialdir="sheets", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
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
            initialdir="sheets", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
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
        