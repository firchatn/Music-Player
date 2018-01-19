from pygame import mixer 

mixer.init()
mixer.music.load('re.mp3')

def playmusic():
    mixer.music.play()
