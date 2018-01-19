from pygame import mixer
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import random

# init variables

ispaused = False

class Handler:
    
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def playmusic(self,play):
        mixer.music.play()

    def stopmusic(self,stop):
        mixer.music.stop()
        
    def pausemusic(self,pause):
        global ispaused
        if ispaused:
            mixer.music.unpause()
            ispaused = False
        else:
            mixer.music.pause()
            ispaused = True
            
    
builder = Gtk.Builder()
builder.add_from_file("player.glade")
builder.connect_signals(Handler())

mixer.init()
mixer.music.load('re.mp3')

window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)
window.set_default_size(700, 300)

image = builder.get_object("image1")
image.set_from_file('player.png')

window.show_all()


Gtk.main()

