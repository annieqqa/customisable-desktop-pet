import tkinter as tk
import time
import random
dialogues=[]

class pet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        
        noOfFrames_idle = 9
        noOfFrames_ideaPop = 53
        noOfFrames_sleeping = 118

        # load gifs from media (Please add your own media folder and add your gifs)
        self.idle = [tk.PhotoImage(file='media/idle.gif', format='gif -index %i' % (i)) for i in range(noOfFrames_idle)] 
        self.ideaPop = [tk.PhotoImage(file='media/idea_pop.gif', format='gif -index %i' % (i)) for i in range(noOfFrames_ideaPop)]
        self.sleeping = [tk.PhotoImage(file='media/sleeping.gif', format='gif -index %i' % (i)) for i in range(noOfFrames_sleeping)]
        
        self.actions = [self.idle, self.ideaPop, self.sleeping]
        
        self.frame_index = 0
        self.frames = self.idle
        self.img = self.idle[self.frame_index] #initialize first image

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
        
        # create a menu with custom features
        # here, "send to lesson" means close window while random windows containing inside jokes (stored in "dialogues") will pop out on clicking "speak"
        m = tk.Menu(self.window, tearoff = 0) 
        m.add_command(label ="Send to lesson", command = self.window.destroy) 
        m.add_command(label ="Speak", command = self.speak)  
        
        # disable drag unless left clicked
        self.dragging = False
        
        self.window.bind('<Button-1>', self.SaveLastClickPos) #detect left click
        self.window.bind('<B1-Motion>', self.Dragging)
        self.window.bind('<ButtonRelease-1>', self.exitDragging)  
        
        self.lastClickX = 0 
        self.lastClickY = 0 
        
        #show menu on right click
        def do_popup(event): 
            try: 
                m.tk_popup(event.x_root, event.y_root) 
            finally: 
                m.grab_release() 
        self.label.bind("<Button-3>", do_popup) 
        

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = 0
        self.y = 0
        self.window.geometry('160x144+%s+%s'%(str(self.x), str(self.y)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts

        self.window.after(0, self.update)
        self.window.mainloop()
        
    def SaveLastClickPos(self,event):
        self.dragging = True
        self.lastClickX = event.x
        self.lastClickY = event.y

    def Dragging(self,event):
        self.dragging = True
        self.x, self.y = event.x - self.lastClickX + self.window.winfo_x(), event.y - self.lastClickY + self.window.winfo_y()
        self.window.geometry('160x144+%s+%s'%(str(self.x), str(self.y)))
    
    def exitDragging(self, event):
        self.dragging = False
        self.update()

    def updateFrames(self):
        self.frames = random.choices(self.actions, weights=[0.5,0.25,0.25], k=1)[0]
        # print(len(choice))

    def update(self):
        # advance frame if 50ms have passed
        if not self.dragging:
            if time.time() >= self.timestamp + 0.2:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                if self.frame_index < len(self.frames)-1:
                    self.frame_index += 1
                    self.img = self.frames[self.frame_index]
                elif self.frame_index == len(self.frames)-1:
                    self.frame_index = 0
                    self.updateFrames()
                    self.img = self.frames[self.frame_index]

            # create the window
            self.window.geometry('160x144+%s+%s'%(self.x, self.y))
            # add the image to our label
            self.label.configure(image=self.img)
            # give window to geometry manager (so it will appear)
            self.label.pack()

            # call update after 10ms
            self.window.after(10, self.update)
        
    def speak(self):
        self.newWindow = tk.Tk()
        self.newWindow.title("Desktop pet says:")
        self.bubble = tk.Label(self.newWindow, text=dialogues[random.randint(0,len(dialogues)-1)])
        self.bubble.pack()

pet()