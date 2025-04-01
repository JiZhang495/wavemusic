import tkinter as tk
from tkinter import filedialog, messagebox
from scripts.music import Music

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

        # Open file link to load score
        self.open_file_button = tk.Button(root, text="Load Score", command=self.load_score)
        self.open_file_button.pack(pady=5)

        # Save score
        self.save_file_button = tk.Button(root, text="Save Score", command=self.save_score)
        self.save_file_button.pack(pady=5)

        # Button for creating WAV
        self.create_wav_button = tk.Button(root, text="Create WAV", command=self.create_wav)
        self.create_wav_button.pack(pady=5)

        # Button for playing WAV
        self.play_button = tk.Button(root, text="Create and Play WAV", command=self.play_wav)
        self.play_button.pack(pady=5)

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
        try:
            Music(score).write_wav(filename="music.wav", sample_rate=44100, bpm=100)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create WAV file: {e}")
        messagebox.showinfo("Info", "WAV file created successfully!")

    def play_wav(self):  
        score = self.score_entry.get(1.0, tk.END).strip()
        if not score:
            messagebox.showwarning("Warning", "Score is empty!")
            return   
        try:
            Music(score).playscore(filename="music.wav", sample_rate=44100, bpm=100)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create/play WAV file: {e}")
            return
