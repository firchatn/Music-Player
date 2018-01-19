from pygame import mixer
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import random
import os

# init variables

ispaused = False





def treeviewItems():
    store = Gtk.ListStore(str)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        store.append ([f])
    #for key, value in docs.items():
    #    store.append ([value])
    treeview.set_model(store)
    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn("Defined User List", rendererText, text=0)
    treeview.append_column(column)


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

progress = builder.get_object("progressbar1")
progress.set_fraction(1)

progress.set_text("player on")
progress.pulse()
treeview = builder.get_object("treeview1")
treeviewItems()
window.show_all()


Gtk.main()

