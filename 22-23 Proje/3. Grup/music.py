import os
import assistant_details as ad
from pathlib import Path

# setup.py dosyasının var olup olmadığını kontrol ediyoruz
my_file = Path("setup.py")
if my_file.is_file():
    import setup
    music_path = setup.music_path
else:
    music_path = 'C:/Users/svimu/Music'

# Müzik dizinindeki şarkıları listeliyoruz
şarkılar = os.listdir(music_path)

def play_music():
    os.startfile(os.path.join(music_path, şarkılar[0]))
    return "Müzik Çalınıyor"

def pause_music():
    return "Windows için mevcut değil"

def stop_music():
    return "Windows için mevcut değil"

def next_song():
    return "Windows için mevcut değil"

def previous_song():
    return "Windows için mevcut değil"

def play_specific_song(song_name):
    return "Windows için mevcut değil"
