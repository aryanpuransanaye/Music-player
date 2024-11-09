from customtkinter import *
from tkinter import * #get button image
import audio_metadata #music cover
from io import BytesIO #music cover
from pygame import mixer #playing music
from mutagen.mp3 import MP3 #music time
from tinytag import TinyTag #muisc tag(title,artist,...)
from tkinter import filedialog #open file
from tktooltip import ToolTip #button's tips
from PIL import Image, ImageTk, ImageFilter, ImageEnhance #background and get hex_color
import os, pygame, time, random, lyricsgenius, threading

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

class GUI():

    def __init__(self):

        self.mainframe = CTkFrame(window, width=600, height = 700, fg_color = "#000000")
        self.searchfram = CTkFrame(window, width=450, height = 100)
        self.playlistfram = CTkScrollableFrame(window, width=425, height = 629, fg_color="#121212")
        self.info_lyricsframe = CTkScrollableFrame(window, width=450, height=700, fg_color="#121212")
        self.buttomframe = CTkFrame(window, height=100, corner_radius=1, fg_color="#000000")
        
        self.soundButton = CTkButton(self.buttomframe, image= volumeupImage, text = "", width = 10, fg_color='transparent', command=self.mute)
        self.volumeSlider = CTkSlider(self.buttomframe, from_=0, to=10, width=100, command=self.soundvalue)
        self.volumeSlider.set(10)

        self.bgimageLabel = CTkLabel(self.mainframe, text = "", width= 600, height=700)
        self.font = CTkFont(family = 'times', size=40)
        self.nameLabel = CTkLabel(self.bgimageLabel, text = "SELECT A PATH\nTHEN ENJOY", font = self.font, fg_color='#000000', bg_color="transparent", width=600)
        self.coveredLabel = CTkLabel(self.bgimageLabel, text = "", image= defultcoverImage)

        self.searchEntry = CTkEntry(self.searchfram, width=220, height=30, placeholder_text="Search...")

        self.skipforwardButton = CTkButton(self.buttomframe, image=skipforwardImage, text="", width=10, fg_color='transparent', command=self.skipforward)
        self.nextbutton = CTkButton(self.buttomframe, image=nextImage, width = 10, text="", fg_color='transparent', command=self.nexttrack)
        self.playButton = CTkButton(self.buttomframe, image=playImage, text="", width=10, fg_color='transparent', command=self.play)
        self.skipbackwardButton = CTkButton(self.buttomframe, image= skipbackImage, width = 10, text="", fg_color='transparent', command=self.skipbackward)
        self.previousButton = CTkButton(self.buttomframe, image=beforImage, width = 10, text="", fg_color='transparent', command=self.previoustrack)

        self.queueButton = CTkButton(self.buttomframe, image=queuedisableImage, width = 2, text="", fg_color='transparent', command = self.showqueue)
        self.sortButton = CTkButton(self.searchfram, image=sortDisableImage, width = 10, text="", fg_color='transparent', command=lambda: threading.Thread(target=self.sortplaylist).start())
        self.shuffleButton = CTkButton(self.buttomframe, image=shuffleDisableImage, width = 10, text="", fg_color='transparent', command=self.shuffle)
        self.loopButton = CTkButton(self.buttomframe, image=loopDisableImage, width = 10, text="", fg_color='transparent', command=self.loop)
        self.lyricsButoon = CTkButton(self.buttomframe, image=lyricsDisableImage, width = 10, text="", fg_color='transparent', command=lambda :threading.Thread(target=self.getlyricistrack).start())
        self.newpathButton = CTkButton(self.searchfram, image=newfoolderDisableImage, width = 10, text="", fg_color='transparent', command=self.choospath)
        self.moreinforamtinButton = CTkButton(self.buttomframe, image=moreinforamtiondisabledImage, width=10, text= "", fg_color='transparent', command=self.information)

        self.musiccurrenttimeLabel = CTkLabel(self.buttomframe, text = "00:00", fg_color='transparent')
        self.timeSlider = CTkSlider(self.buttomframe, from_=0, to=100, width=1200, command=self.setposofduration)
        self.timeSlider.set(0)
        self.musicdurationLabel = CTkLabel(self.buttomframe, text = "00:00", fg_color='transparent')

        self.put_thing()
        self.buttontips()
        self.keyboardshortcut()
        self.get_elapsedtime()
        self.searchEntry.bind("<KeyRelease>", self.updateplaylist_bysearch)

    def put_thing(self):

        self.mainframe.grid(row=0, column=1, sticky = NS)
        self.searchfram.grid(row = 0, column = 0, sticky = NS, ipadx = 48)
        self.playlistfram.grid(row=0, column=0, sticky = S)
        self.info_lyricsframe.grid(row = 0, column = 2, sticky = NS)
        self.buttomframe.grid(row=1, column=0, columnspan=3, sticky = NSEW)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)
        self.bgimageLabel.pack()
        self.coveredLabel.grid(row=0, column =0, sticky = N, pady = 155)
        self.nameLabel.grid(row= 0, column = 0, sticky = S)

        self.searchEntry.grid(row=0, column=0, pady= 20, padx = 20)
        self.sortButton.grid(row = 0, column = 1)
        self.newpathButton.grid(row=0, column=2)


        self.buttomframe.rowconfigure(1, weight=0)
        self.buttomframe.columnconfigure(0, weight=1)
        self.buttomframe.columnconfigure(1, weight=1)
        self.buttomframe.columnconfigure(2, weight=1)

        self.musiccurrenttimeLabel.grid(row=0, column=0, padx = 8)
        self.timeSlider.grid(row=0, column=1)
        self.musicdurationLabel.grid(row=0, column=2, padx = 8)


        self.soundButton.grid(row=1, column=0)
        self.volumeSlider.grid(row=1, column=1, sticky = W)

        self.previousButton.grid(row=1, column=1, sticky=W, padx = 568)
        self.skipbackwardButton.grid(row=1, column=1,sticky=W, padx = 625)
        self.playButton.grid(row=1, column=1, sticky=E, padx = 680)
        self.skipforwardButton.grid(row=1, column=1, sticky=E, padx = 620)
        self.nextbutton.grid(row=1, column=1, sticky=NE, padx = 565)

        self.lyricsButoon.grid(row=1, column = 2, padx = 8)
        self.moreinforamtinButton.grid(row=1, column=1, sticky=E, padx =0)
        self.queueButton.grid(row=1, column=1, sticky=E, padx = 150)
        self.shuffleButton.grid(row=1, column=1, sticky=E, padx = 100)
        self.loopButton.grid(row=1, column = 1, sticky=E, padx = 50)

    def keyboardshortcut(self, event = None):

        def bindletter(master, modifier, letter, function):
            
            if modifier and letter:
                letter = "-" + letter
            
            master.bind("<{}{}>".format(modifier, letter.upper()), function)
            master.bind("<{}{}>".format(modifier, letter.lower()), function)
    
        bindletter(window, modifier = "Control", letter = "i", function = self.information if not informationstatus else self.informationframedestroy)
        bindletter(window, modifier = "Control", letter = "t", function = (lambda x: threading.Thread(target=self.getlyricistrack).start()) if not lyricsstatus else self.lyricsframedestroy)
        bindletter(window, modifier = "Control", letter = "q", function = self.showqueue if not queueshowstatus else self.queuedestroy)
        bindletter(window, modifier = "Control", letter = "o", function = self.choospath)

        bindletter(window, modifier = "Control", letter = "n", function = self.nexttrack)
        window.bind("<Right>", self.skipforward)
        bindletter(window, modifier = "Control", letter = "b", function = self.previoustrack)
        window.bind("<Left>", self.skipbackward)

        window.bind("<Up>",self.increasevolume)
        window.bind("<Down>",self.decreasevolume)

        bindletter(window, modifier = "Control", letter = "l", function = self.loop)
        bindletter(window, modifier = "Control", letter = "h", function = self.shuffle)
        bindletter(window, modifier = "Control", letter = "m", function = self.mute)
        
        if not playstatus:
            window.bind("<Control-space>", self.play)
        else:
            window.bind("<Control-space>", self.pause)
        if pausestatus:
            window.bind("<Control-space>", self.unpause)

    def buttontips(self):

        self.label = CTkLabel(window)
        self.buttontipslist = ["More Information (Ctrl+I)","Music Lyrics (Ctrl+T)", "New Foolder (Ctrl+O)", "Sort Playlist", "Queue (Ctrl+Q)", "Loop (Ctrl+L)", "Shuffle (Ctrl+H)"]
        
        def showbuttontips(button, index):
            
            ToolTip(button, msg = self.buttontipslist[index], delay = 0.01, follow=True, refresh=0.01, x_offset= -20, y_offset= -50)

        # the loop is break when the index is match to a this list and start the function
        for index, button in enumerate([ self.moreinforamtinButton, self.lyricsButoon, self.newpathButton, self.sortButton, self.queueButton, self.loopButton, self.shuffleButton]):
            showbuttontips(button,index)
        
    def choospath(self, event = None):

        global index, playstatus
        
        path = filedialog.askdirectory(title = "CHOOSE SONGS")
        
        if path:
            os.chdir(path)
            self.songs = (os.listdir(path))
            self.defultsongssort = self.songs
            self.tracks = [TinyTag.get(song) for song in self.songs]
            self.sortedplaylist = [(TinyTag.get(song).title, TinyTag.get(song).artist, TinyTag.get(song).album) for song in self.songs]
            #for choose an new path
            if playliststatus:
                    self.playlistdestroy()
                    mixer.music.unload()
                    self.timeSlider.set(0)
            if lyricsstatus:
                    self.textarea.destroy()
                    self.getlyricistrack()
            if informationstatus:
                    for label in self.infolistlabel:
                        label.pack_forget()
                    for tag in self.taglist:
                        tag.pack_forget()
                    self.information()
            if queuestatus:
                self.clearqueue()
            if queueshowstatus:
                self.queuedestroy()
            if playstatus:
                playstatus = False
                self.timeSlider.set(0)
                self.playButton.configure(command = self.play, image = playImage)
                self.keyboardshortcut()

            index = 0 
            self.playlist()
            self.tracks_name_artist_cover_time()
    
        else:
            return
        
    def tracks_name_artist_cover_time(self):
        
        if len(self.tracks[index].title + "\n" + self.tracks[index].artist) >= 45:
            self.font = CTkFont(family = 'times',size=25)
        else:
            self.font = CTkFont(family = 'times',size=40)
        
        self.nameLabel.configure(text = self.tracks[index].title + "\n" + self.tracks[index].artist, font = self.font)

        self.coveredLabel.configure(image = self.resizemusiccover(445,445,1,0,index))
        self.bgimageLabel.configure(image = self.resizemusiccover(750,890,0.7,110,index))
        self.get_time()

    def resizemusiccover(self, width, height, contrast, blur, index):

        self.file_path = "C://Users//aryan//OneDrive//Desktop//project//music player//cover picture//cover.png"
       
        self.metadata=audio_metadata.load(self.songs[index])
            
        if self.metadata == None:
            self.trackbuttons[index].configure(image = defultcoverImage)
        else:
            self.artwork = self.metadata.pictures[0].data 
            self.stream = BytesIO(self.artwork)
            self.img = Image.open(self.stream)

        resized_img = self.img.resize((width, height), Image.Resampling.LANCZOS)
        contrast_img = ImageEnhance.Contrast(resized_img).enhance(contrast)
        blurred_img = contrast_img.filter(ImageFilter.BoxBlur(blur))
        self.newimg = ImageTk.PhotoImage(blurred_img)

        return self.newimg
    
    def upnextlabeldestroy(self):

        global upnextstatus
        upnextstatus = False

        self.upnextlabel.destroy()

    def upnext(self):
            
        global index, upnextstatus
        upnextstatus = True

        index = -1 if index == len(self.songs)-1 else index

        self.upnextcover = self.resizemusiccover(92, 92, 1, 0, index+1)
        self.upnextlabel = Label(self.bgimageLabel, text = "UP NEXT:\n "+ self.tracks[index+1].title +" • "+ self.tracks[index+1].artist, image = self.upnextcover, compound = "left", bg = "#000000", fg = "#ffffff", border = 1, font = ("",17,""))
        self.upnextlabel.grid(row = 0, column = 0, sticky=NW, pady = 5, padx=18)

        if upnextstatus:
            window.after(5000, lambda: self.upnextlabel.destroy())
    
    def sortplaylist(self):

        global sortbyArtiststatus, sortbyAlbumstatus, sortbyTitlestatus, sortbyDefultstatus ,index

        sortedsongs = []
        self.indexaftersort = 0
        self.sortButton.configure(image = sortEnableImage)
        songselectbeforsort = self.songs[index]
        self.playlistdestroy()
        sortedby = ""
        if sortbyArtiststatus:
            #sort by artist
            sortedby = "ARTIST"
            self.sortedplaylist.sort(key = lambda item: item[1])
            # the first loop is for traversing through the sortedplaylist(playlist for sorting) and the secon loop is for traversing through the songs(path of songs) this is same for 3 conditional of sorting
            for sortedsong in self.sortedplaylist:
                for song in self.songs:
                    track = TinyTag.get(song)
                    if (track.artist) in sortedsong and song not in sortedsongs:
                        sortedsongs.append(song)
                        
            sortbyAlbumstatus = True
            sortbyArtiststatus = False
        
        elif sortbyAlbumstatus:
            sortedby = "ALBUM"
            self.sortedplaylist.sort(key = lambda item: item[2])
            for sortedsong in self.sortedplaylist:
                for song in self.songs:
                    track = TinyTag.get(song)
                    if (track.title) in sortedsong and song not in sortedsongs:
                        sortedsongs.append(song)

            sortbyTitlestatus = True
            sortbyAlbumstatus = False

        elif sortbyTitlestatus:
            sortedby = "TITLE"
            self.sortedplaylist.sort(key = lambda item: item[0])
            # the first loop is for traversing through the sortedplaylist(playlist for sorting) and the secon loop is for traversing through the songs(path of songs) this is same for 3 conditional of sorting
            for sortedsong in self.sortedplaylist:
                for song in self.songs:
                    track = TinyTag.get(song)
                    if (track.artist) in sortedsong and song not in sortedsongs:
                        sortedsongs.append(song)
                    
            sortbyDefultstatus = True
            sortbyTitlestatus = False

        elif sortbyDefultstatus:
            sortedby = "DEFULT"
            sortedsongs = self.defultsongssort
            self.sortButton.configure(image = sortDisableImage)
            sortbyArtiststatus = True
            sortbyDefultstatus = False

        self.songs = sortedsongs
        for sortindex in range(len(sortedsongs)):
            if songselectbeforsort == sortedsongs[sortindex]:
                self.indexaftersort = sortindex
        index = self.indexaftersort

        sortedbyLabel = Label(self.searchfram, text = f"SORED BY\n{sortedby}")
        sortedbyLabel.place(x = 480, y = 25)
        window.after(2000, sortedbyLabel.place_forget)
        self.playlist()
        self.playlistupdate(index)

    def playlistdestroy(self):
        
        global playliststatus
        playliststatus = False

        for button in self.trackbuttons:
            button.destroy()
    
    def playlistupdate(self, index):

        for i, button in enumerate(self.trackbuttons):
            if i == index:
                button.configure(fg_color = "#5a5a5a")
            else:
                button.configure(fg_color = "transparent")


    def playbyyplaylist(self, i):

        global index, playstatus, switchtrack
        playstatus = True
        switchtrack = True
        index = i

        self.play()
        self.playlistupdate(int(index))

    def playlist(self):
        
        global playliststatus

        if not playliststatus:
            playliststatus = True
            self.trackbuttons =[]
            font = CTkFont(weight = "bold")

            for song in range(len(self.songs)):
                tracks_title = self.tracks[song].title
                tracks_artist = self.tracks[song].artist

                max_length = len(tracks_title)
                formatted_tracktitle = tracks_title.ljust(max_length)
                finaltext = f"{formatted_tracktitle}\n{tracks_artist}"

                self.trackbutton = CTkButton(self.playlistfram, command = lambda x = song: self.playbyyplaylist(x) ,text =  finaltext, font = font ,width=500, fg_color='transparent', border_width=0, image= self.resizemusiccover(100,100,1,0,song), compound=LEFT, anchor=EW, corner_radius=2)
                self.trackbutton.bind("<Button-3>", lambda event, x = song: self.addtoqueue(x))
                ToolTip(self.trackbutton, msg = "Right Click To Add in Queue",delay = 0.01, follow=True, refresh=0.01, x_offset= -20, y_offset= -50)
                self.trackbutton._image_label.grid(column = 0, sticky=E)
                self.trackbutton.pack(side = TOP)
                
                self.trackbuttons.append(self.trackbutton)
        
        self.trackbuttons[0].configure(fg_color = "#5a5a5a")

    def addtoqueue(self, track):

        global queuestatus
        queuestatus = True

        #the index selected before add a track to queue
        self.beforqueuedindex = index

        if track not in queuetracks:
            queuetracks.append(track)
        
        if queueshowstatus:
            self.trackbuttons[track].pack(side = TOP)
    
    def removefromqueue(self, track):

        global queuestatus
        index = track

        self.queuebuttonslit[queuetracks.index(index)].pack_forget()
        self.queuebuttonslit.pop(queuetracks.index(index))
        queuetracks.remove(index)

        if len(queuetracks) == 0:
            queuestatus = False
            self.queuedestroy()

    def clearqueue(self):
        
        global queuestatus
        queuestatus = False

        queuetracks.clear()
        self.queuedestroy()

    def playbyqueue(self, track):

        global index, playstatus, switchtrack, queuetracks, queuestatus
        playstatus = True
        switchtrack = True
        index = track

        self.play()
        self.playlistupdate(int(index))
        
        self.queuebuttonslit[queuetracks.index(index)].pack_forget()
        self.queuebuttonslit.pop(queuetracks.index(index))
        queuetracks.remove(index)

        if len(queuetracks) == 0:
            queuestatus = False
            self.queuedestroy()
        
    def queuedestroy(self, event = None):
        
        global queueshowstatus

        if queueshowstatus:
            queueshowstatus = False
            
            self.clearqueueButton.destroy()
            for button in self.queuebuttonslit:
                button.pack_forget()
            
            self.queueButton.configure(image = queuedisableImage, command = self.showqueue)
            self.keyboardshortcut()
        
    def showqueue(self, event = None):

        global queueshowstatus
        queueshowstatus = True

        self.queuebuttonslit = []
        showlist = zip(queuetracks, self.trackbuttons)

        self.clearqueueButton = CTkButton(self.info_lyricsframe, text="Clear Queue", command= self.clearqueue, width=500)
        self.clearqueueButton.pack(side = TOP)

        font = CTkFont(weight = "bold")
        for button in dict(showlist):
            queueButton = CTkButton(self.info_lyricsframe, command = lambda x = button: self.playbyqueue(x), text= self.trackbuttons[button].cget("text"), font = font, image= self.resizemusiccover(100,100,1,0,button), width=500, fg_color='transparent', compound=LEFT, anchor=EW, corner_radius=2)
            queueButton.bind("<Button-3>", lambda event, x = button: self.removefromqueue(x))
            queueButton.pack()
            self.queuebuttonslit.append(queueButton)

        self.queueButton.configure(image = queueenableImage, command = self.queuedestroy)
        self.keyboardshortcut()
        
    def play(self, event = None):
        
        global playstatus, index, lyricsstatus, informationstatus

        index = -1 if index == -1 else index
        
        mixer.music.load(self.songs[index]) if switchtrack or not playstatus else None

        if playstatus:
            self.timeSlider.set(0)
            if switchtrack:
                self.tracks_name_artist_cover_time()

        mixer.music.play(start =  self.timeSlider.get() if self.timeSlider.get() != 0 else 0)
        # play for firs time
        playstatus = True

        if upnextstatus:
            self.upnextlabeldestroy()
        if lyricsstatus:
            lyricsstatus = False
            self.textarea.destroy()
            threading.Thread(target=self.getlyricistrack).start()
        if informationstatus:
            informationstatus = False
            for label in self.infolistlabel:
                label.pack_forget()
            for tag in self.taglist:
                tag.pack_forget()
            self.information()

        self.keyboardshortcut()
        self.playButton.configure(image = pauseImage, command = self.pause)
    
    def pause(self, event = None):

        global pausestatus, playstatus
        pausestatus = True
        playstatus = False
     
        mixer.music.pause()

        self.keyboardshortcut()
        self.playButton.configure(image = playImage, command = self.unpause)

    def unpause(self, event = None):

        global pausestatus, playstatus
        pausestatus = False
        playstatus = True

        mixer.music.unpause()

        self.keyboardshortcut()
        self.playButton.configure(image = pauseImage, command = self.pause)
    
    def nexttrack(self, event = None):

        global index, pausestatus, upnextstatus, playstatus, lastshuffleindex, switchtrack, queuestatus
        playstatus = True
        pausestatus = False
        switchtrack = True

        mixer.music.stop()

        if queuestatus:
            index = queuetracks[0]
            #queuetracks.remove(index)
            queuetracks.pop(0)
            if queueshowstatus:   
               self.queuebuttonslit[0].pack_forget()
               self.queuebuttonslit.pop(0)
            if len(queuetracks) == 0:
                queuestatus = False
                self.queuedestroy()
        else:
            if not shufflestatus:
                index += 1 
                if index == len(self.songs):
                    index = 0
            else:
                self.chooseshuffle()
                lastshuffleindex = -2
        
        self.play()
        self.playlistupdate(index)

    def previoustrack(self, event = None):
         
        global index, pausestatus, upnextstatus, playstatus, lastshuffleindex, switchtrack
        playstatus = True
        pausestatus = False
        switchtrack = True

        mixer.music.stop()

        if queuestatus:
            index = self.beforqueuedindex
        else:
            if not shufflestatus:
                index -= 1
            else:
                index = randomtrackselected[lastshuffleindex]
                lastshuffleindex -= 1
                
        self.play()
        self.playlistupdate(index)
        switchtrack = False

    def skipforward(self, event = None):

        if not playstatus:
            self.play()

        mixer.music.pause()
        self.changetime = int(self.timeSlider.get() + 10)
        self.timeSlider.set(int(self.changetime))
        mixer.music.set_pos(int(self.timeSlider.get()))
        mixer.music.unpause()

        if pausestatus:
            self.unpause()

    def skipbackward(self, event = None):

        if int(self.timeSlider.get()) <= 5:
            if mixer.music.get_busy():
               self.play()
        else:
            mixer.music.pause()
            self.changetime = int(self.timeSlider.get() - 10)
            self.timeSlider.set(int(self.changetime))
            mixer.music.set_pos(int(self.timeSlider.get()))
            mixer.music.unpause()
                
            if pausestatus:
                self.unpause()
    
    def loop(self, event = None):

        global loopstatus
        loopstatus = True if not loopstatus else False

        self.loopButton.configure(image = loopEnableImage if loopstatus else loopDisableImage)
        self.keyboardshortcut()

    def chooseshuffle(self, event = None):

        global index
        #this function its for choose random songs the first if its for check if the all of songs are selected once then make clear the random list
        if len(self.songs) != len(randomtrackselected):
            randomchoise = random.randint(0, len(self.songs)-1)
            #this if its for cheking all the randomchoises are diffrent to each other and if they are same the random choice is not append to the list and run the function again
            if randomchoise not in randomtrackselected:
                randomtrackselected.append(randomchoise if randomchoise not in randomtrackselected else self.chooseshuffle())
                index = randomtrackselected[len(randomtrackselected)-1]  
                self.song_mut = MP3(self.songs[index])
            else:
                self.chooseshuffle()
        else:
            randomtrackselected.clear()

    def shuffle(self, event = None):

        global shufflestatus
        shufflestatus = True if not shufflestatus else False

        self.shuffleButton.configure(image = shuffleEnableImage if shufflestatus else shuffleDisableImage)
        self.keyboardshortcut()

    def updateplaylist_bysearch(self, event):

        searchedstr = self.searchEntry.get()
        #when the Entry get character and character is not null do if, else do else
        if searchedstr != "":
            for button in self.trackbuttons:
                if searchedstr.lower() in button.cget("text").lower():
                    button.pack()
                else:
                    button.pack_forget()
        #pack track button by defult
        else:
            for button in self.trackbuttons:
                button.pack_forget()
                button.pack()
        

    def soundvalue(self, event = None):
        
        global volumeset

        mixer.music.set_volume((self.volumeSlider.get()/10))

        volumeset = (self.volumeSlider.get())
             
        self.soundButton.configure(image = muteImage if volumeset == 0 else volumeupImage if volumeset > 5 else volumedownImage)
    #for change volume with UP button 
    def increasevolume(self, event = None):
        
        self.volumeSlider.set(self.volumeSlider.get()+1)   
        mixer.music.set_volume((self.volumeSlider.get()/10))

    def mute(self, event = None):

        global mutestatus
        mutestatus = True if not mutestatus else False
        
        mixer.music.set_volume(0 if mutestatus else volumeset/10)
        self.soundButton.configure(image = muteImage if mutestatus else volumeupImage if volumeset >= 5 else volumedownImage)
        self.keyboardshortcut()
    #for change volume with Down button 
    def decreasevolume(self, event = None):

        self.volumeSlider.set(self.volumeSlider.get()-1)   
        mixer.music.set_volume((self.volumeSlider.get()/10))
    
    def setposofduration(self, event = None):

        if mixer.music.get_busy() or pausestatus:
            self.timeSlider.bind("<Button-1>", lambda x: mixer.music.pause())
            self.timeSlider.bind("<B1-Motion>", lambda x: mixer.music.set_pos(self.timeSlider.get()))
            self.timeSlider.bind("<ButtonRelease-1>", lambda x: mixer.music.unpause() if not pausestatus else None + print("Aa"))
        
        self.musiccurrenttimeLabel.configure(text=time.strftime("%M:%S", time.gmtime(self.timeSlider.get())))

    def get_time(self):
        #get music duration
        self.song_mut = MP3(self.songs[index])
        song_length = self.song_mut.info.length
        self.timeSlider.configure(to = int(song_length))
        #when for first time music is not playing the current time must be 0
        if not playstatus:
            self.current_time = 0
        #update music current time
        if not pausestatus and mixer.music.get_busy():
            self.current_time = mixer.music.get_pos() / 1000
            # get the current time of the song of time silder after playing the song
            if not playstatus and int(self.timeSlider.get()) != 0:
                self.current_time = int(self.timeSlider.get())
            #duration and current time convert to MM:SS
            self.song_length_convert = time.strftime("%M:%S", time.gmtime(song_length))
            self.musicdurationLabel.configure(text = self.song_length_convert)
            
            if int(self.timeSlider.get()) == int(self.current_time):
                self.timeSlider.set(int(self.current_time))
                self.current_time_convert = time.strftime("%M:%S", time.gmtime(int(self.current_time)))
            else:
                self.timeSlider.set(self.timeSlider.get()+1)
            
            self.current_time_convert = time.strftime("%M:%S", time.gmtime(int(self.timeSlider.get())))
            
            self.musiccurrenttimeLabel.configure(text = self.current_time_convert)

            upnexttime = time.strftime("%M:%S", time.gmtime(song_length - self.timeSlider.get()))
            if upnexttime <= "00:30" and not upnextstatus and not  shufflestatus and not loopstatus:
                threading.Thread(target=self.upnext).start()

    def get_elapsedtime(self):

        if playstatus and not pausestatus:
            for event in pygame.event.get():     
                if event.type == MUSIC_END:
                    #play auto next track
                    if not loopstatus: 
                        self.nexttrack() if not mixer.music.get_busy() else None
                    #when loop is true
                    else: 
                        self.play() if not mixer.music.get_busy() else None
        
            self.get_time()
        window.after(1000, self.get_elapsedtime)

    def informationframedestroy(self, event = None):
        
        global informationstatus
        informationstatus = False

        for label in self.infolistlabel:
            label.pack_forget()
        for tag in self.taglist:
            tag.pack_forget()
        
        self.moreinforamtinButton.configure(image=moreinforamtiondisabledImage, command = self.information)
        self.keyboardshortcut()

    def information(self, event = None):

        global informationstatus

        if lyricsstatus:
            self.lyricsframedestroy()

        if not informationstatus:
            self.moreinforamtinButton.configure(image=moreinforamtionenabledImage, command = self.informationframedestroy)
            self.infolistlabel = []
            self.taglist = []
            infolist = ["Title", "Artist", "Album", "Album Artist", "#Track", "Duration", "Genere", "Year", "Bitrate"]
            fontinfo = CTkFont(family="arial", size = 35)
            for i in range(len(infolist)):
                
                maintaglist = [self.tracks[index].title, self.tracks[index].artist, self.tracks[index].album, self.tracks[index].albumartist, self.tracks[index].track, self.song_length_convert, self.tracks[index].genre, self.tracks[index].year, self.tracks[index].bitrate]

                infolabel = CTkLabel(self.info_lyricsframe, text = infolist[i], width=450, font = fontinfo, compound=LEFT)
                infolabel.configure(fg_color = "#181818" if i%2 == 0 else "transparent")
                infolabel.pack()

                fonttag = CTkFont(family="arial", size= 35 if len(str(maintaglist[i])) < 30 else 20)
                taglabel = CTkLabel(self.info_lyricsframe, text = maintaglist[i], width=450, font = fonttag, compound=LEFT, text_color="#b3b3b3")
                taglabel.configure(fg_color = "#181818" if i%2 == 0 else "transparent")
                taglabel.pack()

                self.infolistlabel.append(infolabel)
                self.taglist.append(taglabel)

            informationstatus = True
            self.keyboardshortcut()

    def lyricsframedestroy(self, event = None):

        global lyricsstatus
        lyricsstatus = False

        self.textarea.destroy()
        self.lyricsButoon.configure(image=lyricsDisableImage, command = lambda: threading.Thread(target=self.getlyricistrack).start())
        self.keyboardshortcut()

    def getlyricistrack(self, event = None):

        global lyricsstatus, getlyricsstatus

        if informationstatus:
            self.informationframedestroy()
            
        if not lyricsstatus:
            lyricsstatus = True
            self.lyricsButoon.configure(image=lyricsEnableImage, command = self.lyricsframedestroy)
            font = CTkFont(family="arial", size = 14)
            self.textarea = CTkTextbox(self.info_lyricsframe, height=700, width=450, font = font)
            self.textarea.pack(side=LEFT)

            self.lyrics_track = TinyTag.get(self.songs[index])
            artist = str(self.lyrics_track.artist)
            title = str(self.lyrics_track.title)

            token = "dfN_KUA1Dl4xnTbuUppeM-bo8y0UL6hqifaOWlb_48GbnCcNVU_MCAxj68KUA3KZ"
            genius = lyricsgenius.Genius(token)
            
            try:
                song = genius.search_song(title, artist)
                print(song)
                song_lyrics = song.lyrics if song else print("zzzz")
                getlyricsstatus = True
            except Exception as e:
                getlyricsstatus = False
                print(f"fail{e}")

            if not getlyricsstatus:
                self.textarea.insert(END,"CHECK YOURE CONNECTION\nCLOSE an OPEN TO TRY AGAIN")
            else:
                self.textarea.delete('1.0',END)
                song_lyrics = str(song_lyrics).split("[", 1)
                result = song_lyrics[-1] if len(song_lyrics) > 1 else song_lyrics[0]
                self.textarea.insert(END, "[" + result)
            self.textarea.configure(state='disabled')

            self.keyboardshortcut()
            
if __name__ == "__main__":

    window = CTk()
    window.configure(fg_color = "#000000")

    playImage = PhotoImage(file = "image\\PLAY.png")
    muteImage = PhotoImage(file = "image\\MUTE.png")
    volumeupImage = PhotoImage(file = "image\\VOLUMEUP.png")
    volumedownImage = PhotoImage(file = "image\\VOLUMEDOWN.png")
    lyricsDisableImage = PhotoImage(file = "image\\LYRICSDISABLE.png")
    lyricsEnableImage = PhotoImage(file = "image\\LYRICSENABLE.png")
    newfoolderDisableImage = PhotoImage(file = "image\\NEWFOOLDERDISABLE.png")
    newfoolderEnableImage = PhotoImage(file = "image\\NEWFOOLDERENABLE.png")
    sortDisableImage = PhotoImage(file = "image\\SORTDISABLE.png")
    sortEnableImage = PhotoImage(file = "image\\SORTENABLE.png")
    pauseImage = PhotoImage(file = "image\\PAUSE.png")
    loopDisableImage = PhotoImage(file = "image\\LOOPDISABLE.png")
    loopEnableImage = PhotoImage(file = "image\\LOOPENABLE.png")
    shuffleDisableImage = PhotoImage(file = "image\\SHUFFLEDISABLE.png") 
    shuffleEnableImage = PhotoImage(file = "image\\SHUFFLEENABLE.png") 
    nextImage = PhotoImage(file = "image\\NEXT.png")
    beforImage = PhotoImage(file = "image\\BEFORE.png")
    skipforwardImage = PhotoImage(file = "image\\SKIPFORWARD.png")
    skipbackImage = PhotoImage(file = "image\\SKIPBACK.png")
    searchlistDisableImage = PhotoImage(file = "image\\SEARCHLISTDISABLE.png")
    searchlistEnableImage = PhotoImage(file = "image\\SEARCHLISTENABLE.png")
    defultcoverImage = PhotoImage(file  = "image\\DEFULTMUSICCOVER.png")
    moreinforamtiondisabledImage = PhotoImage(file = "image\\MOREINFORMATIONDISABLE.png")
    moreinforamtionenabledImage = PhotoImage(file = "image\\MOREINFORMATIONENABLE.png")
    queuedisableImage = PhotoImage(file = "image\\QUEUEDISABLE.png")
    queueenableImage = PhotoImage(file = "image\\QUEUEENABLE.png")

    sortbyArtiststatus = True
    sortbyAlbumstatus = False
    sortbyTitlestatus = False
    sortbyDefultstatus = False
    playstatus = False
    pausestatus = False
    shufflestatus = False
    loopstatus = False
    queuestatus = False
    queueshowstatus = False
    mutestatus = False
    switchtrack = False
    upnextstatus = False
    informationstatus = False
    lyricsstatus = False
    playliststatus = False
    getlyricsstatus = True

    index = 0
    volumeset = 10
    randomtrackselected = []
    queuetracks = []
    lastshuffleindex = -2

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    pygame.init()
    MUSIC_END = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(MUSIC_END)

    GUI()

    window.mainloop()
