import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import pygame
import noisereduce as nr
import soundfile as sf
from pydub import AudioSegment

x='1'
root = tk.Tk()

# Initialze Pygame Mixer
pygame.mixer.init()

canvas = tk.Canvas(root, width=400, height=200)
canvas.grid(columnspan=5, rowspan=5)

#logo
logo = Image.open('Team logo.jpg')
logo = logo.resize((400, 300), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=2, row=0)

#instructions
instructions = tk.Label(root, text="Select a .wav file on your computer", font="Arial")
instructions.grid(columnspan=5, column=1, row=1)

def add_song():
    song = askopenfilename(initialdir="/", title='Choose Your .Wav file', filetypes=(("wav files", "*.wav"), ))

	# Add song to listbox
    wav_list.insert(tk.END, song)

# Play selected song
def play():

    global stopped
    stopped = False
    song = wav_list.get(tk.ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)



def stop():

	# Stop Song From Playing
	pygame.mixer.music.stop()
	wav_list.selection_clear(tk.ACTIVE)

def fix():
    global x
    soundlink = wav_list.get(tk.ACTIVE)
    sound = AudioSegment.from_wav(soundlink)
    sound = sound.set_channels(1)
    sound.export("mono"+x+".wav", format="wav")
    data, rate = sf.read("mono"+x+".wav")
    noisy_part = data[0:900000]
    reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)
    sf.write("Fixed"+x+".wav", reduced_noise, rate)  
    wav_list.insert(tk.END, "Fixed"+x+".wav")
    x= int(x) + 1
    x= str(x)
    
    
#browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:add_song(), font="Arial", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=1, row=2,padx=50,pady=10)


#fix
fix_text = tk.StringVar()
fix_btn = tk.Button(root, textvariable=fix_text, command=fix,font="Arial", bg="#20bebe", fg="white", height=2, width=15)
fix_text.set("Fix")
fix_btn.grid(column=3, row=2,padx=50,pady=10)

#playlist
wav_list= tk.Listbox(root,bg='black',fg='green',width=100,selectbackground="green", selectforeground="black")
wav_list.grid(column=2,row=3,pady=20)

# Create Player Control Frame
controls_frame = tk.Frame(root)
controls_frame.grid(row=4, column=2, pady=20)

#buttons
play_btn = Image.open('play.png')
play_btn = play_btn.resize((80, 80), Image.ANTIALIAS)
play_btn_img = ImageTk.PhotoImage(play_btn)
pause_btn = Image.open('pause.png')
pause_btn = pause_btn.resize((80, 80), Image.ANTIALIAS)
pause_btn_img = ImageTk.PhotoImage(pause_btn)
play_button = tk.Button(controls_frame, command=play,image=play_btn_img, borderwidth=0, )
pause_button = tk.Button(controls_frame, command=stop,image=pause_btn_img, borderwidth=0, )
play_button.grid(row=0, column=0, padx=20)
pause_button.grid(row=0, column=1, padx=20)

canvas = tk.Canvas(root, width=400, height=50)
canvas.grid(columnspan=5)

root.mainloop()
