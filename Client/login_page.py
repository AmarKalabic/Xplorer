# -*- coding: utf-8 -*-

import sys, Tkinter
sys.modules['tkinter'] = Tkinter
import os
import os.path
from tkinter import *
import tkMessageBox
import PIL.Image as Image
import PIL.ImageTk as ImageTk

import _mysql


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

app.geometry('300x170+200+200') # set new geometry

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
img_fake = "%s/img/login.png"%rootdir
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

var3 = StringVar()
e3 = Entry(app, textvariable=var3, width=20)
e3.place(x=120, y=45)

var3.set("")

username = var3.get()

labelText2 = StringVar()
labelText2.set("Username")
label3 = Label(app, textvariable=labelText2, height=1, bg="white", fg="black")
label3.place(x=50, y=45)
#label3.pack()

#checkBoxVal = IntVar()
#checkBox1 = Checkbutton(app, variable=checkBoxVal, text="Happy?")
#checkBox1.pack()

var2 = StringVar()
entry = Entry(app, width=20, textvariable=var2)
entry.place(x=120, y=90)

var2.set("")

labelText3 = StringVar()
labelText3.set("Password")
label4 = Label(app, textvariable=labelText3, height=1, bg="white", fg="black")
label4.place(x=50, y=88)

def beenClicked():
    if var3.get() != "": #username
       if var2.get() != "": #password
          #connect na bazu i check
          print "This is var3:", var3.get()
          try:
             db=_mysql.connect(host="127.0.0.1",user="root",
                       passwd="test123",db="brix_test", port=3306)
          except:
              tkMessageBox.showerror("Xplorer 1.0 Login", "No connection to database. Please contact administrator!")
          db.query("""SELECT USERNAME FROM usernames
                   WHERE USERNAME="%s" LIMIT 1"""%var3.get())
          result = db.store_result()
          result1 = result.fetch_row()
          print "Username:"
          print result1
          if (var3.get(),) in result1:
              db.query("""SELECT PASSWORD FROM usernames
                       WHERE PASSWORD=PASSWORD("%s") LIMIT 1"""%var2.get())
              result2 = db.store_result()
              result3 = result2.fetch_row()
              print "Password:"
              print result3
              if result3:
                  app.destroy()
                  root.destroy()
                  execfile("client.py")
                  sys.exit()
              else:
                  tkMessageBox.showerror("Xplorer 1.0 Login", "Password you entered is incorrect.")
          else:
              tkMessageBox.showerror("Xplorer 1.0 Login", "Username you entered is incorrect.")
       else:
           tkMessageBox.showerror("Xplorer 1.0 Login", "Please enter your password.")
    else:
        tkMessageBox.showerror("Xplorer 1.0 Login", "Please enter your username.")
    return

button1 = Button(app, text="Login", width=20, command=beenClicked)
button1.place(x=100, y=120)

app.mainloop()