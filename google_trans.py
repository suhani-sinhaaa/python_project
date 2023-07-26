import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import pygame
import time
import random

def translate_text():
    src_lang = combo_s.get()
    dest_lang = combo_d.get()
    text_to_translate = source_txt.get(1.0, tk.END)

    translator = Translator()
    translated = translator.translate(text_to_translate, src=src_lang, dest=dest_lang)
    translated_text.set(translated.text)

    # Set the translated text in the dest_txt widget
    dest_txt.delete(1.0, tk.END)
    dest_txt.insert(tk.END, translated.text)

def speak(text):
    tts = gTTS(text=text, lang='en')
    output_file = os.path.join(os.path.expanduser("~"), f"translated_audio_{time.time()}.mp3")
    tts.save(output_file)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)

    # Play the audio
    pygame.mixer.music.play()

    # Schedule the function to check if the audio is still playing
    check_audio(output_file)


def check_audio(output_file, remove_event):
    for event in pygame.event.get():
        if event.type == remove_event:
            # Remove the audio file after playback is complete
            remove_audio(output_file)

    if pygame.mixer.music.get_busy():
        root.after(100, check_audio, output_file, remove_event)  # Check again after 100 milliseconds

def remove_audio(output_file):
    os.remove(output_file)


root = tk.Tk()
root.title(" Google Translator")
root.geometry("1000x1000")
root.config(bg="linen")

frame = tk.Frame(root, bg="dark sea green", padx=20, pady=20)
frame.pack(pady=20)

label_title = tk.Label(frame, text="TRANSLATOR", font=("Times New Roman", 40, "bold"),bg="antique white")
label_title.grid(row=0, column=0, columnspan=5, pady=10)

label_src = tk.Label(frame, text="Source Language:", font=("Times New Roman", 16),bg="antique white")
label_src.grid(row=1, column=0, padx=10, pady=10)

combo_s = ttk.Combobox(frame, value=list(LANGUAGES.values()), font=("Times New Roman", 16))
combo_s.grid(row=1, column=1, padx=10, pady=10)
combo_s.set("English")

label_dest = tk.Label(frame, text="Destination Language:", font=("Times New Roman", 16), bg="antique white")
label_dest.grid(row=1, column=2, padx=10, pady=10)

combo_d = ttk.Combobox(frame, value=list(LANGUAGES.values()), font=("Times New Roman", 16))
combo_d.grid(row=1, column=3, padx=10, pady=10)
combo_d.set("Hindi")

source_txt = tk.Text(frame, font=("Times New Roman", 20), wrap=tk.WORD, width=60, height=8)
source_txt.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

translate_button = tk.Button(frame, text="Translate", font=("Times New Roman", 16), bg="antique white", command=translate_text)
translate_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

dest_txt = tk.Text(frame, font=("Times New Roman", 20), wrap=tk.WORD, width=60, height=8)
dest_txt.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

translated_text = tk.StringVar()
text_output = ttk.Label(frame, textvariable=translated_text, font=("Times New Roman", 16), wraplength=700, anchor="center", background="light cyan")
text_output.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

voice_button = tk.Button(frame, text="Listen", font=("Times New Roman", 16), bg="antique white", command=lambda: speak(translated_text.get()))
voice_button.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()
