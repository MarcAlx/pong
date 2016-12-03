#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-
# Developed by Marc-Alexandre Blanchard

from tkinter import *
from math import *
import os,tkinter.messagebox,random,time

class Application(object):
    """ qBall """
    _Version,_Name=1.0,"qBall"
    _CHECKTIME,_MOVETIME,_SPEEDTIME,_WIDTH,_HEIGHT,_MATRIXWIDTH,_MATRIXHEIGHT,_BLOCKSIZE,_BALLSIZE,_canMove1,_canMove2=50,75,5,1080,720,36,22,30,20,True,True
    _MATRIX,_RDV=[],[]
    angle = 45
    vitesse = 5
    defballx = -2*_BALLSIZE
    defbally = -2*_BALLSIZE
    ballX = 0
    ballY = 0
    minX = -2*_BALLSIZE
    minY = -2*_BALLSIZE
    maxX = int(_BLOCKSIZE*_MATRIXWIDTH-3*_BALLSIZE)
    maxY = int(_BLOCKSIZE*_MATRIXHEIGHT-3*_BALLSIZE)
    _POSX1,_POSY1=1,12
    _POSX2,_POSY2=34,12

    def __init__(self):
        self._tk = Tk()
        self._tk.protocol("WM_DELETE_WINDOW", self.onQuit)
        self._tk.title(self._Name)
        self.createMenuBar()
        self._tk.lift()
        self._tk.resizable(width=False, height=False)
        
        self.initStat()

        self._blockUp = Frame(self._tk)
        self._Score=Label(self._blockUp, text="0",textvariable=self._SCORE1,font=("Lucida", 25),width=10)
        self._Score.pack(side = LEFT)
        self.boutonStart = Button(self._blockUp,text="Start", command=lambda n='': self.start())
        self.boutonStart.pack(side = LEFT)
        self._Score=Label(self._blockUp, text="0",textvariable=self._SCORE2,font=("Lucida", 25),width=10)
        self._Score.pack(side = LEFT)
        self._blockUp.pack()

        self._blockMiddle = Frame(self._tk)
        self._FRAME = Canvas(self._blockMiddle, width=self._BLOCKSIZE*self._MATRIXWIDTH, height=self._BLOCKSIZE*self._MATRIXHEIGHT, bg="black")
        if(sys.platform.startswith("darwin")):
            self._tk.bind_all('<Command-q>',self.quit)
            self._tk.bind_all('<Command-Q>',self.quit)
        self._FRAME.bind_all('<Key>',self.onKeyPress)
        self._FRAME.bind_all('<Up>',self.onUpPress)
        self._FRAME.bind_all('<Down>',self.onDownPress)
        self._FRAME.pack()
        self._blockMiddle.pack()

        self.init()

    def mainloop(self):
        self._tk.mainloop()
    
    def about(self):
        tkinter.messagebox.showinfo("About", "Developed by\n\nMarc-Alexandre Blanchard\n\nmarc.alexandre.blanchard.pro@gmail.com")
    
    def createMenuBar(self):
        self.menubar = Menu(self._tk)
        self.appmenu = Menu(self.menubar, tearoff=0)
        self.appmenu.add_command(label="Start", command=lambda n='': self.start())
        self.appmenu.add_command(label="Quit", command=self._tk.destroy)
        self.menubar.add_cascade(label=self._Name, menu=self.appmenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.helpmenu.add_command(label="Help & How-To", command=self.help)
        self.helpmenu.add_command(label="Version", command=self.version)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self._tk.config(menu=self.menubar)
    
    def help(self):
        tkinter.messagebox.showinfo("Help & How-To", "About : A\nHelp & How-To : H\nVersion : V\n\nMove : Q D ← →\n\nRestart : R\n")
    
    def onKeyPress(self,event):
        if(event.char=="q" or event.char=="Q"):
            self.toTheLeft()
        elif(event.char=="d" or event.char=="D"):
            self.toTheRight()
        elif(event.char=="a" or event.char=="A"):
            self.about()
        elif(event.char=="h" or event.char=="H"):
            self.help()
        elif(event.char=="v" or event.char=="V"):
            self.version()
        elif(event.char=="r" or event.char=="R"):
            self.init()
        elif(event.char=="z" or event.char=="Z"):
            self.up1()
        elif(event.char=="s" or event.char=="S"):
            self.down1()

    def onUpPress(self,event):
    	self.up2()

    def onDownPress(self,event):
    	self.down2()
    
    def onQuit(self):
        self.cancelation()
        self._tk.destroy()

    def quit(self,event):
        self.onQuit()

    def version(self):
        tkinter.messagebox.showinfo("Version", "Version "+str(self._Version))

    def draw(self):
        self._FRAME.delete(ALL)
        for i in range (0,self._MATRIXHEIGHT,1):
            for j in range(0,self._MATRIXWIDTH,1):
                if(self._MATRIX[i][j]==0):
                    self._FRAME.create_rectangle((self._BLOCKSIZE*j),(self._BLOCKSIZE*i),((self._BLOCKSIZE*j)+self._BLOCKSIZE),((self._BLOCKSIZE*i)+self._BLOCKSIZE),fill="black")
                elif(self._MATRIX[i][j]==1):
                    self._FRAME.create_rectangle((self._BLOCKSIZE*j),(self._BLOCKSIZE*i),((self._BLOCKSIZE*j)+self._BLOCKSIZE),((self._BLOCKSIZE*i)+self._BLOCKSIZE),fill="white",tag=("_Block"+j+'_'+i))            
    
    def drawbar1(self):    
        self._FRAME.create_rectangle(self._POSX1*self._BLOCKSIZE,self._POSY1*self._BLOCKSIZE,((self._POSX1*self._BLOCKSIZE)+self._BLOCKSIZE),((self._POSY1+4)*self._BLOCKSIZE),fill="white",tag=("_BAR1"))

    def drawbar2(self):
        self._FRAME.create_rectangle(self._POSX2*self._BLOCKSIZE,self._POSY2*self._BLOCKSIZE,((self._POSX2*self._BLOCKSIZE)+self._BLOCKSIZE),((self._POSY2+4)*self._BLOCKSIZE),fill="white",tag=("_BAR2"))

    def drawBallP1(self):
        self.vitesse=5
        self.drawcircle(50,50,1,(self._POSY1+1),self._BALLSIZE)

    def drawBallP2(self):
        self.vitesse=-5
        self.drawcircle(50,50,32,(self._POSY2-2),self._BALLSIZE)

    def drawcircle(self,x,y,posX,posY,rad):
        self._FRAME.delete("BALL")
        self._FRAME.move("BALL",-self.ballX,-self.ballY)
        self.ballX=posX*self._BLOCKSIZE
        self.ballY=posY*self._BLOCKSIZE
        self._FRAME.create_oval(x-rad,y-rad,x+rad,y+rad,width=1,fill='white',tag=("BALL"))
        self._FRAME.move("BALL",self.ballX,self.ballY)

    def fillMatrix(self):
        for i in range (0,self._MATRIXHEIGHT+1,1):
            self._MATRIX.append([])
            for j in range(0,self._MATRIXWIDTH,1):
                self._MATRIX[i].append(0)

    def cancelation(self):
        for i in self._RDV:
            self._FRAME.after_cancel(i)

    def move(self):
        futureX=self.ballX+int(self.vitesse*cos(radians(self.angle)))
        futureY=self.ballY+int(self.vitesse*sin(radians(self.angle)))

        if(futureX>self.maxX):
            self.score1PP()
            self.drawBallP2()
        elif(futureX<self.minX):
            self.score2PP()
            self.drawBallP1()
        elif(futureY>self.maxY):
            self.angle=(180-self.angle)%361+random.randint(1,5)
            self.vitesse=-self.vitesse
        elif(futureY<self.minY):
            self.angle=(self.angle-90)%361+random.randint(1,5)
            self.vitesse=-self.vitesse
        elif(futureX<30 and (futureY>=(self._POSY1-2)*self._BLOCKSIZE and futureY<=(self._POSY1+2)*self._BLOCKSIZE)):
            self.angle=(self.angle-90)%361+random.randint(1,5)
            self.vitesse=-self.vitesse
        elif(futureX>950 and (futureY>=(self._POSY2-2)*self._BLOCKSIZE and futureY<=(self._POSY2+2)*self._BLOCKSIZE)):
            self.angle=(360-self.angle)%361+random.randint(1,5)
            self.vitesse=-self.vitesse

        futureX=self.ballX+int(self.vitesse*cos(radians(self.angle)))
        futureY=self.ballY+int(self.vitesse*sin(radians(self.angle)))

        self._FRAME.move("BALL",futureX-self.ballX,futureY-self.ballY)

        self.ballX = futureX
        self.ballY = futureY

        self._RDV.append(self._FRAME.after(self._SPEEDTIME,lambda a = 1,b = 1 : self.move()))

    def init(self):
        self._MATRIX = []
        self.fillMatrix()
        self.draw()
        self.drawbar1()
        self.drawbar2()

    def start(self):
        self.cancelation()
        self.resetstat()
        p=random.randint(1,2)
        if(p==1):
        	self.drawBallP1()
        elif(p==2):
        	self.drawBallP2()
        self.move()

    def initStat(self):
        self._SCORE1,self._SCORE2=IntVar(),IntVar()
        self._SCORE1.set(0)
        self._SCORE2.set(0)

    def resetstat(self):
        self._SCORE1.set(0)
        self._SCORE2.set(0)

    def down1(self):
        if(self._POSY1<self._MATRIXHEIGHT-4):
            self._POSY1+=1
            self._FRAME.move("_BAR1",0,self._BLOCKSIZE)
            self._RDV.append(self._FRAME.after(self._MOVETIME,self.allowMove1))

    def up1(self):
        if(self._POSY1>=1):
            self._POSY1-=1
            self._FRAME.move("_BAR1",0,-self._BLOCKSIZE)
            self._RDV.append(self._FRAME.after(self._MOVETIME,self.allowMove1))

    def down2(self):
        if(self._POSY2<self._MATRIXHEIGHT-4):
            self._POSY2+=1
            self._FRAME.move("_BAR2",0,self._BLOCKSIZE)
            self._RDV.append(self._FRAME.after(self._MOVETIME,self.allowMove2))

    def up2(self):
        if(self._POSY2>=1):
            self._POSY2-=1
            self._FRAME.move("_BAR2",0,-self._BLOCKSIZE)
            self._RDV.append(self._FRAME.after(self._MOVETIME,self.allowMove2))

    def allowMove1(self):
        self._canMove1=True

    def allowMove2(self):
        self._canMove2=True

    def score1PP(self):
        self._SCORE1.set(int(self._SCORE1.get())+1)

    def score2PP(self):
        self._SCORE2.set(int(self._SCORE2.get())+1)

if __name__ == '__main__':
    Application().mainloop()
