import tkinter as tk
import pyautogui
import time
import random
from dialogues import *

class pet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()

        # placeholder image
        self.idle = [tk.PhotoImage(file='media/idle.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.ideaPop = [tk.PhotoImage(file='media/idea_pop.gif', format='gif -index %i' % (i)) for i in range(4)]
        
        self.actions = [self.idle, self.ideaPop]
        
        self.frame_index = 0
        self.img = self.idle[self.frame_index]

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)

        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')
        
        m = tk.Menu(self.window, tearoff = 0) 
        m.add_command(label ="Send to lesson", command = self.window.destroy) 
        m.add_command(label ="Speak", command = self.speak) 
        # m.add_command(label ="Move", command = self.move) 
        # m.add_command(label ="Laugh", command = self.laugh)  
        
        self.window.bind('<Button-1>', self.SaveLastClickPos)
        self.window.bind('<B1-Motion>', self.Dragging)  
        
        self.lastClickX = 0 
        self.lastClickY = 0 
        
        def do_popup(event): 
            try: 
                m.tk_popup(event.x_root, event.y_root) 
            finally: 
                m.grab_release() 
        self.label.bind("<Button-3>", do_popup) 
        

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = 0
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update, self.idle)
        self.window.mainloop()
        
    def SaveLastClickPos(self,event):
        self.lastClickX = event.x
        self.lastClickY = event.y


    def Dragging(self,event):
        x, y = event.x - self.lastClickX + self.window.winfo_x(), event.y - self.lastClickY + self.window.winfo_y()
        self.window.geometry("+%s+%s" % (x , y))    
            
    
        
        
    #make window movable
    def move(self):
        self.window.bind("<ButtonPress-1>", self.start_move)
        self.window.bind("<ButtonRelease-1>", self.stop_move)
        self.window.bind("<B1-Motion>", self.do_move)

    def updateFrames(self,frames):
        return random.choices(self.actions, weights=[0.9, 0.1], k=1)[0]

    def update(self, frames):
        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.05:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            if self.frame_index < len(frames)-1:
                self.frame_index = self.frame_index + 1
                self.img = frames[self.frame_index]
            elif self.frame_index == len(frames)-1:
                self.frame_index = 0
                frames = self.updateFrames(frames)
                self.img = frames[self.frame_index]

        # create the window
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(10, self.update, self.idle)
        
    def speak(self):
        self.newWindow = tk.Tk()
        self.newWindow.title("Paulinian buddy says:")
        self.bubble = tk.Label(self.newWindow, text=dialogues[random.randint(0,2)])
        self.bubble.pack()
    
    def start_move(self,event):
        self.x = event.x
        self.y = event.y
    
    def stop_move(self, event):
        self.x = self.window.winfo_x()
        self.y = self.window.winfo_y()

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")
        
pet()