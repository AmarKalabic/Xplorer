# -*- coding: utf-8 -*-

import httplib
import threading
import httplib2
import os
import random
import sys
import time

import sys, Tkinter
sys.modules['tkinter'] = Tkinter
import TkTreectrl as treectrl
import subprocess
import pythoncom, pyHook
import os
import win32api, win32con
from win32api import GetSystemMetrics
import os.path
import ConfigParser
import time
from tkinter import *
import tkMessageBox
import PIL
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import time
from tkFileDialog import askopenfilename

import urllib2
import requests
from bs4 import BeautifulSoup



if hasattr(sys, 'frozen'):
  # retrieve path from sys.executable
  rootdir = os.path.abspath(os.path.dirname(sys.executable))
else:
  # assign a value from __file__
  rootdir = os.path.abspath(os.path.dirname(__file__))

class NewRoot(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.attributes('-alpha', 0.0)

class MyMain(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.overrideredirect(1)
        self.attributes('-topmost', 1)
        self.geometry('+100+100')
        ############################## self.bind('<ButtonRelease-3>', self.on_close)  #right-click to get out

    def on_close(self, event):
        self.master.destroy()

def beenClicked():
    global app
    a = tkMessageBox.showinfo("Xplorer 1.0", "Thanks for using Xplorer 1.0")
    time.sleep(3)
    app.destroy()
    root.destroy()
    return

def changeLabel():
    name = "Thanks for the click " + yourName.get()
    labelText.set(name)
    yourName.delete(0, END)
    yourName.insert(0, "Test")
    return

root = NewRoot()
root.lower()
root.iconify()
root.title('Xplorer 1.0')
app = MyMain(root)
#app.configure(background='#000000')
app.resizable(0,0)
root.wm_iconbitmap('%s/img/logo_16x16.ico'%rootdir)

def move_window(event):
    app.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

def clickedX():
    app.destroy()
    root.destroy()
    sys.exit()

app.overrideredirect(True) # turns off title bar, geometry

app.geometry('850x455+200+200') # set new geometry

# make a frame for the title bar
title_bar = Frame(app, bg='white', relief='raised', bd=2)

# put a close button on the title bar
img_path = "%s/img/x_button.png"%rootdir
x_button_img = ImageTk.PhotoImage(Image.open(img_path))
close_button = Button(title_bar, image=x_button_img, command=clickedX, bd=0)
close_button.image = x_button_img

labelText = StringVar()
labelText.set("Xplorer 1.0")
label1 = Label(title_bar, textvariable=labelText, height=1, bg="white", fg="black")
label1.place(x=1, y=-3)

# a canvas for the main area of the window
###img_path = "%s/img/logo.gif"%rootdir
###img = ImageTk.PhotoImage(Image.open(img_path))
img_fake = "%s/img/bg.png"%rootdir
img = ImageTk.PhotoImage(Image.open(img_fake))
width1 = img.width()
height1 = img.height()
window = Canvas(app, bg='black', width=width1, height=height1)

window.create_image(width1/2.0, height1/2.0, image=img)
window.update()


# pack the widgets
title_bar.pack(expand=1, fill=X)
close_button.pack(side=RIGHT)
window.pack(expand=1, fill=BOTH)
#window.create_image(0, 0, image=img, anchor="nw")

# bind title bar motion to the move window function
title_bar.bind('<B1-Motion>', move_window)
#imgPath = '%s/img/volume+-_16x16.gif'%rootdir
#photo = PhotoImage(file = imgPath)
#label = Label(image = photo)
#label.image = photo
#label.grid(row = 3, column = 1, padx = 5, pady = 5)
#2 img = PhotoImage(file='%s/img/volume+-_16x16.png'%rootdir)
#2 app.tk.call('wm', 'iconphoto', app._w, img)
#app.iconbitmap(default='%s/img/volume+-_16x16.ico'%rootdir)
app.title("Xplorer 1.0")

"""def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)

s = Scrollbar(app, bg="black") 
L = Listbox(app, bg="white", width=50, activestyle="dotbox", highlightcolor="green", highlightthickness=1.5, selectmode="SINGLE") 
L.bind('<<ListboxSelect>>', onselect)
s.place(x=750, y=35)
L.place(x=300, y=35)

#s.pack(side=RIGHT, fill=Y) 
#L.pack(side=LEFT, fill=Y) 

s.config(command=L.yview) 
L.config(yscrollcommand=s.set) """

labelText1 = StringVar()
labelText1.set("Double-click file to download...")
label11 = Label(app, textvariable=labelText1, height=2, bg="#DF1A2B", fg="white")
label11.place(x=300, y=200)

def select_cmd(selected):
    print 'Selected items:', selected

def download_file(url):
        #url = tuple[2]
        #url = str(tuple[2])
        file_name = url.split('/')[-1]
        print "File - name: ", file_name
        u = urllib2.urlopen(url)
        if not isinstance(file_name, unicode):
           file_name1 = file_name.decode("utf-8")
        else:
            file_name1 = file_name
        f = open("./downloads/" + file_name1.replace("%20", " "), 'wb')
        meta = u.info()
        #print "Meta: ", meta
        #print "Content-Length: ", meta.getheaders("Content-Length")
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s" % (file_name)
        os.system('cls')
        file_size_dl = 0
        block_sz = 8192
        while True:
            app.update()
            buffer = u.read(block_sz)
            if not buffer:
               break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            #print status,
            time.sleep(.2)
            labelText1.set(status,)
            tuple = (file_name, status)
        f.close()
        onEnd()

"""canvas = Label(app) #ili Canvas(app)
text = canvas.create_text(18, 18, font="Purisa", text="Status: Double-click file to download...")
canvas.place(x=50, y = 50)"""

"""def download_file(url):
        u = urllib2.urlopen(url)
        file_name = url.split('/')[-1]
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        #print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 1024*50 #50 kb
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"[%3.2f%%]" % (file_size_dl * 100. / file_size)
            text="Status: downloading..."+status
            labelText.set(text)

        f.close()

        onEnd()"""

"""def initUI(self):

        self.pack(fill=app.BOTH, expand=1)

        canvas = app.Canvas(self)

        self.text = canvas.create_text(18,18,anchor=tk.W,font="Purisa",text="Status: Double-click file to download...")
        canvas.create_window((270,18),window=but)

        canvas.pack(fill=tk.BOTH, expand=1)
        self.canvas=canvas"""

def onEnd():
    labelText1.set("Status: done!")


def getSoup(plus_path):
    global getzz
    if plus_path != None:
       print "Plus path in getSoup is NOT NONE! It's:"
       getz = 'http://192.168.1.2:8000/' + plus_path
       if "..." in getz:
           getzz.replace("...", "")
       else:
           getzz = getz
       print "This is getz:", getzz
       requestz = requests.get(getzz)
    else:
       requestz = requests.get('http://192.168.1.2:8000')
    try:
       html_page = requestz
       soup = BeautifulSoup(html_page.text)
       return soup
    except requests.exceptions.ConnectionError, e:
       print "Error:\n", e
       tkMessageBox.showerror("Error!", "Cannot connect to server, contact administrator!")


def getUnicodeLink(name, folder, plus_path):
    global soup
    print "This is folder", folder
    if folder == True:
       """Folder handling!"""
       if name != "...":
          print "Its folder and not ...!"
          soup = getSoup(plus_path)
       else:
          print "Its folder and ...!"
          plus_path = ""
          soup = getSoup(plus_path)
    else:
       print "Its not folder!"
       plus_pathz = None
       soup = getSoup(plus_pathz)
    #DEBUGGER: print "This is soup:"
    #DEBUGGER: print soup
    links = soup.find_all('a', href=True)
    for z in links:
        filename = z.get_text().split(".")[0]
        href = z['href'].replace(" ", "%20")
        link = "http://192.168.1.2:8000/" + href
        #DEBUGGER: print filename, " == ", name
        if filename.encode("utf-8") == name:
           unicode_url = link.encode("utf-8")
           return unicode_url


currentpath = StringVar()
currentpath.set("This is your current path: ./files/")
currentpath_label = Label(app, textvariable=currentpath, height=2, bg="#DF1A2B", fg="white", width = 50)
currentpath_label.place(x=300, y=330)


def double_clicked(clicked):
    print "Double clicked item: ", clicked
    tuple = mlb.get(clicked)[0]
    unicode_name = tuple[0].encode("utf-8")
    #unicode_url = getUnicodeLink(unicode_name)
    #u = urllib2.urlopen(unicode_url)
    #meta = u.info()
    #file_size = int(meta.getheaders("Content-Length")[0])
    if tuple[1] != "Folder" and tuple[1] != "Double-click this to go folder back":
       is_folder = False
       #plus_path = unicode_name.replace(" ", "%20")
       plus_path = ""
       unicode_url = getUnicodeLink(unicode_name, is_folder, plus_path)
       u = urllib2.urlopen(unicode_url)
       meta = u.info()
       file_size = int(meta.getheaders("Content-Length")[0])
       try:
          t = threading.Thread(target=download_file(unicode_url))
          t.start()
       except urllib2.HTTPError, e:
           print e
           tkMessageBox.showalert("File not found!", "File not found on the server! If you think this is not your fault, contact administrator!")
    else:
        if tuple[1] != "...":
           """Back folder handling goes here"""
           mlb.delete("end", 0)
           mlb.insert('end', "...", "Double-click this to go folder back", "/")
           is_folder = True
           plus_path = unicode_name.replace(" ", "%20")
           print "This is plus_path:"
           print plus_path
           print "This is unicode_name:"
           print unicode_name
           unicode_url = getUnicodeLink(unicode_name, is_folder, plus_path)
           #real_unicode_url = unicode_url.replace(".../", "")
           print "This is unicode_url:"
           print unicode_url
           #real_plus_path = unicode_url.replace(plus_path, "")
           print "This is getSoup:"
           print getSoup(plus_path)
           files = getSoup(plus_path).find_all('li')
           links = getSoup(plus_path).find_all('a', href=True)
           filedict = {

                     }
           iffirst = True
           for z in links:
                filename = z.get_text()
                href = z['href'].replace(" ", "%20")
                link = "http://192.168.1.2:8000/" + plus_path + href
                print "THIS IS MASTER LINK:"
                print link
                filedict[filename] = link
           for filename in filedict:
               link = filedict.get(filename).encode("utf-8")
               if "." in filename:
                  filename_noex1 = filename.split('.')
                  filename_noexreal1 = filename_noex1[0]
                  extension = filename_noex1[1]
                  print "This is link:", link
                  try:
                     u1 = urllib2.urlopen(link)
                  except urllib2.HTTPError:
                     link = "http://192.168.1.2:8000/" + href
                  if iffirst == True:
                     first_link = link
                     iffirst = False
                     currentpath_from_link = ""
                     num = -1
                     for i in link.split("/"):
                         num += 1
                         print "This is num:", num
                         currentpath_from_link_now = first_link.split("/")[num]
                         if num >= 3:
                            currentpath_from_link += "/" + currentpath_from_link_now
                     currentpath_from_link.replace("%20", " ")
                            #currentpath_from_link = link.split("/")[3]
                     print 15 * "/"
                     print "This is currentpath from link:"
                     print currentpath_from_link
                     print 15 * "/"
                     currentpath.set("This is your current path: ." + currentpath_from_link)
                     print "This is no plus_path link:"
                     print plus_path
                     u1 = urllib2.urlopen(link.encode("utf-8"))
                  meta1 = u1.info()
                  file_size = int(meta1.getheaders("Content-Length")[0])
                  real_file_size = 0
                  if file_size >= 1048567:
                     while file_size > 0:
                           file_size = file_size - 1048567
                           real_file_size += 1
                     real_file_size = real_file_size, "MB"
                  elif (file_size >= 1024):
                       while file_size >0:
                             file_size = file_size - 1024
                             real_file_size += 1
                       real_file_size = real_file_size, ",", file_size, "KB"
                  else:
                      real_file_size = file_size, "bytes"
                  mlb.insert('end', filename_noexreal1, getExtension(extension), real_file_size) #*map(filename_noexreal, getExtension(extension)
                  print "not dir: ", filename
               else:
                    mlb.insert('end', filename, "Folder", "/") #filename + "\\", ""
                    print "is dir: ", filename
        else:
             """Here goes folder handling"""
             mlb.delete("end", 0)
             mlb.insert('end', "...", "Double-click this to go folder back", "/")
             is_folder = True
             plus_path= unicode_name.replace(" ", "%20")
             #unicode_url = getUnicodeLink(unicode_name, is_folder, plus_path)
             print "This is plus_path:"
             print plus_path
             print "This is getSoup:"
             print getSoup(plus_path)
             files = getSoup(plus_path).find_all('li')
             links = getSoup(plus_path).find_all('a', href=True)
             filedict = {

                 }

             for z in links:
                filename = z.get_text()
                href = z['href'].replace(" ", "%20")
                link = "http://192.168.1.2:8000/"+ plus_path + href
                filedict[filename] = link
             for filename in filedict:
                 link = filedict.get(filename).encode("utf-8")
                 if "." in filename:
                    filename_noex1 = filename.split('.')
                    filename_noexreal1 = filename_noex1[0]
                    extension1 = filename_noex1[1]
                    print "This is link:", link
                    u1 = urllib2.urlopen(link)
                    meta1 = u1.info()
                    file_size = int(meta1.getheaders("Content-Length")[0])
                    real_file_size = 0
                    if file_size >= 1048567:
                       while file_size > 0:
                             file_size = file_size - 1048567
                             real_file_size += 1
                       real_file_size = real_file_size, "MB"
                    elif (file_size >= 1024):
                       while file_size >0:
                             file_size = file_size - 1024
                             real_file_size += 1
                       real_file_size = real_file_size, ",", file_size, "KB"
                    else:
                        real_file_size = file_size, "bytes"
                    """currentpath_from_link = link.split("/")[0]
                    print 15 * "/"
                    print "This is currentpath from link:"
                    print currentpath_from_link
                    print 15 * "/"""
                    #currentpath.set("This is your current path: ." + currentpath_from_link)
                    mlb.insert('end', filename_noexreal1, getExtension(extension), real_file_size) #*map(filename_noexreal, getExtension(extension)
                    print "not dir1: ", filename
                 else:
                    mlb.insert('end', filename, "Folder", "/") #filename + "\\", ""
                    print "is dir: ", filename





mlb = treectrl.MultiListbox(app)
mlb.place(x=300, y=35)
mlb.focus_set()
mlb.configure(selectcmd=select_cmd, selectmode='extended', height=150, width=450, command=double_clicked)
mlb.config(columns=('Name', 'Description', 'Download Size'))

#path = "C:/"

lista = []

def getExtension(extension):
    dictionary = {"exe":"Win. executable",
                  "zip":"Zip file",
                  "rar":"Rar Archive",
                  "txt":"Text file",
                  "doc":"MS Word 97-2003 document",
                  "docx":"MS Word Document",
                  "pdf":"PDF",
                  "html":"Hypertext Markup Language file",
                  "html":"Hypertext Markup Language",
                  "php":"PHP file",
                  "jpg":"JPG Image",
                  "jpeg":"JPEG Image",
                  "png":"PNG Image",
                  "bmp":"BMP Image",
                  "gif":"Animated GIF Image",
                  "tiff":"TIFF Image",
                  "cdr":"Corel DRAW File",
                  "psd":"PhotoShop File",
                  "wmv":"Windows Media File",
                  "mp3":"MP3 File",
                  "mp4":"MP4 File",
                  "avi":"Audio Video Interleave",
                  "mpg":"MPEG-1 Video",
                  "ppt":"MS PowerPoint Presentation",
                  "wav":"Waveform Audio Format",
                  "mov":"QuickTime MOV",
                  "ai":"Adobe Illustrator Document",
                  "xls":"MS Excel Spreadsheet",
                  "pps":"PowerPoint Show",
                  "dwg":"AutoCAD File",
                  "swf":"SWF vector graphics",
                  "dat":"Data",
                  "mdb":"MS Access",
                  "rm":"RealMedia",
                  "jar":"Java Archive",
                  "dmg":"Disk Image",
                  "dvf":"Sony Compressed Voice File",
                  "flv":"Flash Video",
                  "iso":"Optical disk image",
                  "wpd":"WordPerfect Document",
                  "7z":"7zip archive",
                  "gz":"Gzip archive",
                  "fla":"Adobe Flash",
                  "rtf":"Rich Text Format",
                  "msi":"Windows Installer",
                  "divx":"DivX video",
                  "bin":"Binary File",
                  "mswmm":"Win. Movie Maker Project",
                  "tgz":"Archive; WinZipNT - TAR - GNUzip",
                  "log":"Log file",
                  "dll":"Dynamic-link library",
                  "mcd":"MathCad file; MathCad",
                  "eml":"E-mail message",
                  "ogg":"Ogg file",
                  "mid":"Musical Instrument Digital Interface",
                  "torrent":"BitTorrent",
                  "lnk":"Computer Shortcut (This should not be here since it does nothing)",
                  "mp2":"MPEG-1 Audio Layer II",
                  "bat":"Batch file",
                  "sh":"Linux shell script",
                  "bup":"Backup file",
                  "sql":"Structured Query Language",
                  "java":"Java file",
                  "class":"Java Class file",
                  "py":"Python file",
                  "pas":"Pascal file",
                  "cpp":"C++ file",
                  "cc":"C++ file",
                  "css":"Cascading Style Sheets",
                  "rb":"Ruby file"
                  }

    if dictionary.get(extension) != None:
        filedesc = dictionary.get(extension)
        return filedesc
    else:
        filedesc = "No description"
        return filedesc

def getSoupFirst():
    try:
       html_page = requests.get('http://192.168.1.2:8000')
       soup = BeautifulSoup(html_page.text)
       return soup
    except requests.exceptions.ConnectionError, e:
        print "Error:\n", e
        tkMessageBox.showerror("Error!", "Cannot connect to server, contact administrator!")

#soup = BeautifulSoup(html_page.text)

def showHome():

    files = getSoupFirst().find_all('li')
    links = getSoupFirst().find_all('a', href=True)

    filedict = {

    }

    for z in links:
        filename = z.get_text()
        href = z['href'].replace(" ", "%20")
        link = "http://192.168.1.2:8000/" + href
        filedict[filename] = link
        #print z.get_text()
        #print "a href: ", z['href']


    for filename in filedict:
        link = filedict.get(filename).encode("utf-8")
        if "." in filename:
           filename_noex = filename.split('.')
           filename_noexreal = filename_noex[0]
           extension = filename_noex[1]
           u = urllib2.urlopen(link)
           meta = u.info()
           file_size = int(meta.getheaders("Content-Length")[0])
           real_file_size = 0
           if file_size >= 1048567:
              while file_size > 0:
                    file_size = file_size - 1048567
                    real_file_size += 1
              real_file_size = real_file_size, "MB"
           elif (file_size >= 1024):
              while file_size >0:
                    file_size = file_size - 1024
                    real_file_size += 1
              real_file_size = real_file_size, ",", file_size, "KB"
           else:
               real_file_size = file_size, "bytes"
           mlb.insert('end', filename_noexreal, getExtension(extension), real_file_size) #*map(filename_noexreal, getExtension(extension)
           print "not dir: ", filename
        else:
           mlb.insert('end', filename, "Folder", "/") #filename + "\\", ""
           print "is dir: ", filename

firsttime = True
if firsttime == True:
   showHome()
   firsttime = False
else:
    pass

"""var1 = StringVar()
e1 = Entry(app, textvariable=var1, bg="black", fg="white", width=40)
e1.place(x=350, y=35)


var1.set("GAMERS.ba YT Klip #1")

video_title = var1.get()

labelText = StringVar()
labelText.set("Ime video klipa")
label1 = Label(app, textvariable=labelText, height=2, bg="#DF1A2B", fg="white")
label1.place(x=250, y=25)
#label1.pack()

var2 = StringVar()
e2 = Entry(app, textvariable=var2, width=40)
e2.place(x=350, y=65)

video_desc = var2.get()

labelText1 = StringVar()
labelText1.set("Opis video klipa")
label2 = Label(app, textvariable=labelText1, height=2, bg="#DF1A2B", fg="white")
label2.place(x=250, y=55)
#label2.pack()

var3 = StringVar()
e3 = Entry(app, textvariable=var3, width=40)
e3.place(x=350, y=95)

var3.set("gamersba, gaming, games, gameplay")

video_keywords = var3.get()

labelText2 = StringVar()
labelText2.set("Keywords")
label3 = Label(app, textvariable=labelText2, height=2, bg="#DF1A2B", fg="white")
label3.place(x=250, y=85)
#label3.pack()

#checkBoxVal = IntVar()
#checkBox1 = Checkbutton(app, variable=checkBoxVal, text="Happy?")
#checkBox1.pack()

#custName = StringVar(None)
#yourName = Entry(app, textvariable=custName)
#yourName.pack()

def open_file():
    global content
    global file_path
    global filename

    filename = askopenfilename()
    file_path = os.path.dirname(filename)
    entry.delete(0, END)
    entry.insert(0, filename)
    return filename

global entry

entry = Entry(app, width=50, textvariable="Path do filea")
entry.grid(row=0,column=1,padx=2,pady=2,sticky='we',columnspan=25)
entry.place(x=230, y=308)

Button(app, text="Browse", command=open_file).place(x=550, y=305)
#buttonbrowse.place(x=350, y=308)

def start_upload():
    PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "upload_video.py"))
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
       #upload_video.makeitreal()
       upload_video.initialize_upload()
    else:
        tkMessageBox.showerror(
            "Greska!",
            "Ne mogu naci upload skriptu!"
        )
        return

button1 = Button(app, text="START", width=20, command=start_upload)
button1.place(x=355, y=420)"""

app.mainloop()

# c:/Python27/python.exe c:/Users/Amar/Documents/youtube_uploader/START.py