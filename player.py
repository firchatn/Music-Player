from pygame import mixer
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import random
import os
import json

# init variables

ispaused = False
pathdata = 'data/playlist.json'
store = Gtk.ListStore(str)

#     methods

def opend():
    if doesFileExists(path):
        json_data=open(path)
        statistics = json.load(json_data)
    else:
        statistics = {"default": 1}
        with open(path, 'w') as outfile:
            json.dump(statistics, outfile)
    return statistics

def openplaylist():
    json_data=open(pathdata)
    docs = json.load(json_data)
    return docs

def updateplaylist(choice):
    store.append([choice])
    

def choicefile(openfile):
    filter = Gtk.FileFilter()
    filter.set_name("Music")
    filter.add_mime_type("mp3")
    filter.add_pattern("*.mp3")
    global imageschoice
    dialog = Gtk.FileChooserDialog("Please choose a file", window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    dialog.add_filter(filter)
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        pass
    elif response == Gtk.ResponseType.CANCEL:
        return False
    choice = dialog.get_filename()
    docs = openplaylist()
    print(len(docs))
    docs[str(len(docs)+1)] = choice
    with open(pathdata, 'w') as outfile:
            json.dump(docs, outfile)
    updateplaylist(choice)
    dialog.destroy()
    progress.set_text(choice)
    mixer.music.load(choice)
    return choice

def treeviewItems():
    
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    #for f in files:
    #    store.append ([f])
    playlistitems = openplaylist()
    for key, value in playlistitems.items():
        print(key , value)
        store.append([value])
    treeview.set_model(store)
    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn("PlayList", rendererText, text=0)
    treeview.append_column(column)

def progressplus():
    if mixer.music.get_busy():
        new_value = progress.get_fraction() + 0.02
        progress.set_fraction(new_value)
        
# class Handler Sginals

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def playmusic(self,play):
        mixer.music.play()
        progressplus()

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
            
    def setvolume(self, volume,nb = 1,n = 2):
        v = vb.get_value()
        mixer.music.set_volume(v)

def initprogress():
    progress.set_fraction(1)
    progress.set_text("player on")
    progress.set_show_text(True)
    progress.pulse()

def initvoulume():
    v = vb.set_value(1)
    mixer.music.set_volume(1)
#        Main        

builder = Gtk.Builder()
builder.add_from_file("player.glade")
builder.connect_signals(Handler())

mixer.init()
mixer.music.load('data/re.mp3')

window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)
window.set_default_size(700, 300)

image = builder.get_object("image1")
image.set_from_file('images/player.png')

openfile = builder.get_object("imagemenuitem2")
openfile.connect("activate", choicefile)

progress = builder.get_object("progressbar1")
initprogress()
progressplus()

treeview = builder.get_object("treeview1")
treeviewItems()

vb = builder.get_object("volume")
initvoulume()

window.show_all()
Gtk.main()

