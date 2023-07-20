from cmu_112_graphics import *
import random
import math

class WhiteKey(object):
    keys = {0:"B2",1:"C2",2:"Db2",3:"D2",4:"Eb2",5:"E2",6:"F2",7:"Gb2",8:"G2",9:"Ab2",10:"A2",\
            11:"B1",12:"C1",13:"Db1",14:"D1",15:"Eb1",16:"E1",17:"F1",18:"Gb1",19:"G1",20:"Ab1",21:"A1"}
    def __init__(self,app,text,fontDims,x,y,width,height,keyNum,keyNote):
        self.app = app
        self.keyNum = keyNum
        self.keyNote = keyNote
        self.text = text
        self.fontDims = fontDims
        self.font = f"Helvetica {int(self.fontDims)}"
        self.image = self.app.loadImage("WhiteKey.png")
        self.midCImage = self.app.loadImage("MidCKey.png")
        self.w,self.h = width,height        # width,height
        self.wr,self.hr = self.w/2,self.h/2     # radii
        x1,y1 = 0,0
        x2,y2 = self.w,self.h
        self.image = self.image.crop((x1,y1,x2,y2))
        self.midCImage = self.midCImage.crop((x1,y1,x2,y2))
        self.image = self.app.scaleImage(self.image,1)
        self.x,self.y = x,y
        self.location = (self.x-self.wr,self.y-self.hr,self.x+self.wr,self.y+self.hr)

class BlackKey(WhiteKey):
    def __init__(self,app,text,fontDims,x,y,width,height,keyNum,keyNote):
        super().__init__(app,text,fontDims,x,y,width,height,keyNum,keyNote)
        self.image = self.app.loadImage("BlackKey.png")
        x1,y1 = 0,0
        x2,y2 = self.w,self.h
        self.image = self.image.crop((x1,y1,x2,y2))
        self.image = self.app.scaleImage(self.image,1)

class MusicNote(object):
    def __init__(self,app,staffLine,difficulty,keyNum,keyNote):
        self.app = app
        self.keyNum = keyNum
        self.keyNote = keyNote
        self.staffLine = staffLine
        self.difficulty = difficulty
        self.image = self.app.loadImage("musicNote.png")
        x1,y1 = 0,0
        x2,y2 = 400,500
        self.image = self.image.crop((x1,y1,x2,y2))
        self.image = self.app.scaleImage(self.image, 1/5)
        dx = self.app.width/15
        self.x = self.app.width 
        sy,sdy = self.app.gameMode.sy,self.app.gameMode.sdy
        correction = y2/11
        self.y = sy + staffLine*sdy - correction
        # print(f"keyNote = {self.keyNote} keyNum = {self.keyNum}")
     

class Scales(object):
    # 0,1,3,5,6,8,10,12,13,15,17,18,20,22,24
    cMajor = {0:"B",1:"A",3:"G",5:"F",6:"E",8:"D",10:"C",11:"B",13:"A",15:"G",17:"F",18:"E",20:"D",22:"C",\
                    23:"B"}
    fMajor = {0:"Bb",1:"A",3:"G",5:"F",6:"E",8:"D",10:"C",12:"Bb",13:"A",15:"G",17:"F",18:"E",20:"D",22:"C",\
                    24:"Bb"}
    bFlatMajor = {0:"Bb",1:"A",3:"G",5:"F",7:"Eb",8:"D",10:"C",12:"Bb",13:"A",15:"G",17:"F",19:"Eb",20:"D",22:"C",\
                    24:"Bb"}
    eFlatMajor = {0:"Bb",2:"Ab",3:"G",5:"F",7:"Eb",8:"D",10:"C",12:"Bb",14:"Ab",15:"G",17:"F",19:"Eb",20:"D",22:"C",\
                    24:"Bb"}
    aFlatMajor = {0:"Bb",2:"Ab",3:"G",5:"F",7:"Eb",9:"Db",10:"C",12:"Bb",14:"Ab",15:"G",17:"F",19:"Eb",21:"Db",22:"C",\
                    24:"Bb"}
    dFlatMajor = {0:"Bb",2:"Ab",4:"Gb",5:"F",7:"Eb",9:"Db",10:"C",12:"Bb",14:"Ab",16:"Gb",17:"F",19:"Eb",21:"Db",22:"C",\
                    24:"Bb"}
    gFlatMajor = {0:"Bb",2:"Ab",4:"Gb",5:"F",7:"Eb",9:"Db",11:"Cb",12:"Bb",14:"Ab",16:"Gb",17:"F",19:"Eb",21:"Db",23:"Cb",\
                    24:"Bb"}
    cFlatMajor = {0:"Bb",2:"Ab",4:"Gb",6:"Fb",7:"Eb",9:"Db",11:"Cb",12:"Bb",14:"Ab",16:"Gb",18:"Fb",19:"Eb",21:"Db",23:"Cb",\
                    24:"Bb"}

    

class GameMode(Mode):
    def appStarted(self):
        self.setUpStaff()
        self.setUpFlatIndicators()
        self.numOfTiles = 25
        self.notesHit = 0
        self.musicImage = self.loadImage("music.png")
        self.setUpTrebleSymbol()
        self.setUpNotes()
        self.pickRandomScale()
        self.stopWatch = 0
        self.setUpDifficulty()
        self.app.settingsMode = SettingsMode(self.app)
        self.setUpBackGround()
        self.setUpKeys()
        self.paused = False
        self.labelsOn = "on"
    
    def pickRandomScale(self):
        scales = [Scales.cMajor,Scales.fMajor,Scales.bFlatMajor,Scales.eFlatMajor,\
                Scales.aFlatMajor,Scales.dFlatMajor,Scales.gFlatMajor,Scales.cFlatMajor]
        self.scale = random.choice(scales)
        self.getScaleName()
        self.getScaleFlatIndicators()
        self.scaleNums = [num for num in self.scale]
        self.scaleNumsCopy = sorted(self.scaleNums[:])
        self.scaleConverter = dict()        # keyNum
        for i in range(self.numOfSpacesAndLines):
            self.scaleConverter[i] = self.scaleNumsCopy[0]
            self.scaleNumsCopy.pop(0)

    
    def getScaleFlatIndicators(self):
        if self.scale == Scales.cMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = False,False,False
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = False,False,False,False
        elif self.scale == Scales.fMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = True,False,False
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = False,False,False,False
        elif self.scale == Scales.bFlatMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = True,True,False
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = False,False,False,False
        elif self.scale == Scales.eFlatMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = True,True,True
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = False,False,False,False
        elif self.scale == Scales.aFlatMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = True,True,True
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = True,False,False,False
        elif self.scale == Scales.dFlatMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = True,True,True
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = True,True,False,False
        elif self.scale == Scales.gFlatMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = True,True,True
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = True,True,True,False
        elif self.scale == Scales.cFlatMajor:
            self.isbFlat,self.iseFlat,self.isaFlat = True,True,True
            self.isdFlat,self.isgFlat,self.iscFlat,self.isfFlat = True,True,True,True

    def setUpFlatIndicators(self):
        self.flatIndicator = self.loadImage("flatIndicator.png")
        x1,y1 = 0,0
        x2,y2 = 250,350
        self.isbFlat,self.iseFlat,self.isaFlat = False,False,False
        self.isdFlat,self.isgFlat,self.iscFlat = False,False,False
        self.flatIndicator = self.flatIndicator.crop((x1,y1,x2,y2))
        self.flatIndicator = self.scaleImage(self.flatIndicator, 1/2)

    def getScaleName(self):
        self.scaleName = None
        if self.scale == Scales.cMajor:
            self.scaleName = "C Major"
        elif self.scale == Scales.fMajor:
            self.scaleName = "F Major"
        elif self.scale == Scales.bFlatMajor:
            self.scaleName = "B Flat Major"
        elif self.scale == Scales.eFlatMajor:
            self.scaleName = "E Flat Major"
        elif self.scale == Scales.aFlatMajor:
            self.scaleName = "A Flat Major"
        elif self.scale == Scales.dFlatMajor:
            self.scaleName = "D Flat Major"
        elif self.scale == Scales.gFlatMajor:
            self.scaleName = "G Flat Major"
        elif self.scale == Scales.cFlatMajor:
            self.scaleName = "C Flat Major"

    def setUpDifficulty(self):
        self.maxDifficulty = 32
        self.difficulty = 15        # initial difficulty
        self.timeBetweenNotes = self.maxDifficulty - self.difficulty      # edit this for speed of the notes


    def setUpTrebleSymbol(self):
        self.trebleSymbol = self.loadImage("trebleSymbol.png")
        x1,y1 = 0,0
        x2,y2 = 250,350
        self.trebleSymbol = self.trebleSymbol.crop((x1,y1,x2,y2))
        self.trebleSymbol = self.scaleImage(self.trebleSymbol, 17/24)
    

    def setUpKeys(self):
        self.printablepntd = {0:"B",1:"C",2:"Db",3:"D",4:"Eb",5:"E",6:"F",7:"Gb",8:"G",9:"Ab",10:"A",\
            11:"Bb",12:"B",13:"C",14:"Db",15:"D",16:"Eb",17:"E",18:"F",19:"Gb",20:"G",21:"Ab",22:"A",\
            23:"Bb",24:"B",25:"C",26:"Db",27:"D",28:"Eb",29:"E",30:"F",31:"Gb",32:"G",33:"Ab",34:"A"}

        self.pntd = {0:"A1",1:"Bb1",2:"B1",3:"C1",4:"Db1",5:"D1",6:"Eb1",7:"E1",8:"F1",9:"Gb1",10:"G1",11:"Ab1",12:"A2",13:"Bb2",\
                    14:"B2",15:"C2",16:"Db2",17:"D2",18:"Eb2",19:"E2",20:"F2",21:"Gb2",22:"G2",23:"Ab2",24:"A3",25:"Bb3"}

        self.pnty = 9*self.app.height/10        # piano note titles
        self.pntx1 = self.app.width/50
        self.whiteKeys = [ ]
        self.blackKeys = [ ]
        #(self,app,text,fontDims,x,y,width,height)
        fontDims = 15
        self.pntdx = self.app.width/25      # 25
        dy = self.app.height/10        #10
        width = self.app.width/30       #30
        height = self.app.height/6      #6
        whiteKeyIndexes = [0,1,3,5,6,8,10,12,13,15,17,18,20,22,24]
        self.numOfTiles = 25
        for i in range(self.numOfTiles):
            if i in whiteKeyIndexes:
                keyNum = (23-i)%25
                if keyNum == 24:
                    if self.scale == Scales.cMajor:     # fixes bug
                        keyNum = 0
                    else:
                        keyNum = 0
                keyNote = self.printablepntd[i]
                x = self.pntx1+i*self.pntdx
                y = self.pnty-dy
                newWhiteKey = WhiteKey(self.app,self.printablepntd[i],fontDims,x,y,width,height,keyNum,keyNote)
                self.whiteKeys.append(newWhiteKey)
            else:
                blackKeyDy = 1.25*dy
                blackKeyHeight = 0.85*height
                keyNum = (23-i)%25
                keyNote = self.printablepntd[i]
                x = self.pntx1+i*self.pntdx
                y = self.pnty-blackKeyDy
                newBlackKey = BlackKey(self.app,self.printablepntd[i],fontDims,x,y,width,blackKeyHeight,keyNum,keyNote)
                self.blackKeys.append(newBlackKey)

    def setUpBackGround(self):
        self.backgroundImage = self.loadImage("lightGray.png")
        self.backgroundImage = self.app.scaleImage(self.backgroundImage,3)

    def setUpNotes(self):
        self.notes = [ ]
        self.ndx = 10       # note speed

    def setUpStaff(self):
        self.numOfStaffLines = 7
        self.numOfSpacesAndLines = (self.numOfStaffLines*2)       # 14
        self.sx1,self.sx2 = 0,self.app.width
        self.sy = self.app.height/6
        self.sdy = self.app.height/30

    def createNewNotes(self):
        if self.stopWatch % self.timeBetweenNotes == 1:
            flag = False
            while flag == False:
                try:
                    line = random.randint(0,self.numOfSpacesAndLines)
                    keyNum = self.scaleConverter[line]
                    keyNote = self.scale[keyNum]
                    # print(line,keyNum,keyNote)
                    newNote = MusicNote(self.app,line,self.difficulty,keyNum,keyNote)
                    self.notes.append(newNote)
                    flag = True
                except:
                    flag = False


    def mousePressed(self,event):
        for whiteKey in self.whiteKeys:
            x1,y1,x2,y2 = whiteKey.location
            if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
                # print(f"key pressed = {whiteKey.keyNote}, keyNum = {whiteKey.keyNum}")
                for note in self.notes:
                    if note.keyNum == whiteKey.keyNum:
                        self.notes.remove(note)
                        self.notesHit += 1
                        return

        for blackKey in self.blackKeys:
            x1,y1,x2,y2 = blackKey.location
            if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
                # print(f"key pressed = {blackKey.keyNote}, keyNum = {blackKey.keyNum}")
                for note in self.notes:
                    if note.keyNum == blackKey.keyNum  and note.keyNote == blackKey.keyNote:
                        self.notes.remove(note)
                        self.notesHit += 1
                        return



    def timerFired(self):
        if self.paused:
            return
        self.stopWatch += 1
        self.moveNotes()
        self.createNewNotes()
        # if self.stopWatch % 1000 == 0:
        #     self.pickRandomScale()      # change the scale


    def keyPressed(self,event):
        if event.key == "p":
            self.paused = not self.paused
        elif event.key == "i":
            self.app.setActiveMode(self.app.settingsMode)


    def moveNotes(self):
        if self.paused:
            return
        for note in self.notes:
            note.x -= self.ndx
            if note.x < -15:
                self.notes.remove(note)


    def redrawAll(self,canvas):
        canvas.create_image(self.app.width/2,self.app.height/2, image=ImageTk.PhotoImage(self.backgroundImage))
        canvas.create_image(self.app.width/30,37*self.app.height/100, image=ImageTk.PhotoImage(self.trebleSymbol))
        canvas.create_text(self.app.width/2,self.app.height/25,text=f"Scale: {self.scaleName}",font=f"Helvetica {int(self.app.width/23)} bold")
        canvas.create_text(91*self.app.width/100,2*self.app.height/100,text="(push 'i' to go to settings)")
        canvas.create_text(10*self.app.width/100,7*self.app.height/100,text=f"Notes Hit: {self.notesHit}",font=f"Helvetica {int(self.app.width/40)}")
        if self.paused:
            canvas.create_text(self.app.width/2,self.app.height/2,text="Paused",font=f"Helvetica {int(self.app.width/30)}")
        self.drawStaff(canvas)
        # self.drawNotes(canvas)
        if self.labelsOn == "on":
            self.drawPianoNoteTitles(canvas)
        self.drawKeys(canvas)
        self.drawFlatIndicators(canvas)
        self.drawNotes(canvas)

    
    def drawFlatIndicators(self,canvas):
        sy,sdy = self.sy,self.sdy
        correction = self.app.height/23     # MusicNote: y2/11
        x1 = 13*self.app.width/100
        dx = self.app.width/70
        if self.isbFlat:
            staffLine = 7
            y = sy + staffLine*sdy + correction
            canvas.create_image(x1+0*dx,y, image=ImageTk.PhotoImage(self.flatIndicator))
        if self.iseFlat:
            staffLine = 4
            y = sy + staffLine*sdy + correction
            canvas.create_image(x1+1*dx,y, image=ImageTk.PhotoImage(self.flatIndicator))
        if self.isaFlat:
            staffLine = 8
            y = sy + staffLine*sdy + correction
            canvas.create_image(x1+2*dx,y, image=ImageTk.PhotoImage(self.flatIndicator))
        if self.isdFlat:
            staffLine = 5
            y = sy + staffLine*sdy + correction
            canvas.create_image(x1+3*dx,y, image=ImageTk.PhotoImage(self.flatIndicator))
        if self.isgFlat:
            staffLine = 9
            y = sy + staffLine*sdy + correction
            canvas.create_image(x1+4*dx,y, image=ImageTk.PhotoImage(self.flatIndicator))
        if self.iscFlat:
            staffLine = 6
            y = sy + staffLine*sdy + correction
            canvas.create_image(x1+5*dx,y, image=ImageTk.PhotoImage(self.flatIndicator))
        if self.isfFlat:
            staffLine = 10
            y = sy + staffLine*sdy + correction
            canvas.create_image(x1+6*dx,y, image=ImageTk.PhotoImage(self.flatIndicator))



    def drawKeys(self,canvas):
        for whiteKey in self.whiteKeys:
            if whiteKey.keyNum == 22:
                canvas.create_image(whiteKey.x,whiteKey.y, image=ImageTk.PhotoImage(whiteKey.midCImage)) 
            else:
                canvas.create_image(whiteKey.x,whiteKey.y, image=ImageTk.PhotoImage(whiteKey.image))
        for blackKey in self.blackKeys:
            canvas.create_image(blackKey.x,blackKey.y, image=ImageTk.PhotoImage(blackKey.image))

    def drawPianoNoteTitles(self,canvas):
        for i in range(self.numOfTiles):
            canvas.create_text(self.pntx1+i*self.pntdx,self.pnty,text=self.printablepntd[i])
            


    def drawStaff(self,canvas):
        for staffLine in range(self.numOfStaffLines):
            if staffLine in [0,6]:
                canvas.create_line(self.sx1,self.sy+(staffLine*2*self.sdy),self.sx2,self.sy+(staffLine*2*self.sdy),dash=(10,50))
            else:
                canvas.create_line(self.sx1,self.sy+(staffLine*2*self.sdy),self.sx2,self.sy+(staffLine*2*self.sdy))
        x = 22*self.app.width/100       # draw line at the end of the flat indicators
        y1 = self.sy + 2*self.sdy
        y2 = self.sy + 10*self.sdy
        canvas.create_line(x,y1,x,y2,width=2)



    def drawNotes(self,canvas):
        for note in self.notes:
            canvas.create_image(note.x,note.y, image=ImageTk.PhotoImage(note.image))


class Button(object):
    def __init__(self,x,y,w,h,font="Helvetica 15",fill="white"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = font
        self.fill = fill
        self.x1 = self.x - (1/2)*self.w
        self.x2 = self.x + (1/2)*self.w
        self.y1 = self.y - (1/2)*self.h
        self.y2 = self.y + (1/2)*self.h
        self.location = (self.x1,self.y1,self.x2,self.y2)


# def setUpDifficulty(self):
#         difficultyRange = 10     # variable
#         self.difficulty = self.getUserInput(f"From 1-{difficultyRange}, how close together should the notes be?")      # changes only distance between notes
#         # speedRange = 3
#         # self.speedOfNotes = int(self.getUserInput(f"From 1-{speedRange}, how fast should the notes be?"))        # changes speed
#         dif = 4     # difficulty coeficient
#         self.difficulty = dif*(((difficultyRange-int(self.difficulty))%difficultyRange)+1)
#         self.increasingDifficulty = 1      # can increase over time (but isn't yet)
#         self.timeBetweenNotes = self.increasingDifficulty*self.difficulty       # edit this for speed of the notes

class SettingsMode(Mode):
    def __init__(self,app,**kwargs):
        self.app = app
        self.buttonToGameMode = "g"
        self.i = 0
        self.bigButtonHeight = self.app.height/7
        self.scales = [Scales.cMajor,Scales.fMajor,Scales.bFlatMajor,Scales.eFlatMajor,\
                Scales.aFlatMajor,Scales.dFlatMajor,Scales.gFlatMajor,Scales.cFlatMajor]    #TODO
        self.makeDBetweenButton()
        self.makeScaleButton()
        self.makeLabelsOnButton()
        self.makeSpeedButton()
        super().__init__(**kwargs)

    def makeDBetweenButton(self):
        y = 20*self.app.height/100
        x = self.app.width/2
        w,h = 44*self.app.width/100,self.bigButtonHeight
        font = f"Helvetica {int(self.app.width/30)} bold"
        fill = "light blue"
        self.dBetweenButton = Button(x,y,w,h,font,fill)

        x = (50+35)*self.app.width/100
        w,h = self.app.width/10,self.app.height/10
        text = "+"
        font = f"Helvetica {int(self.app.width/50)} bold"
        fill = "blue"
        self.dBetweenPlusButton = Button(x,y,w,h,font,fill)

        x = (50-35)*self.app.width/100
        text = "-"
        self.dBetweenMinusButton = Button(x,y,w,h,font,fill)

    def makeScaleButton(self):
        y = 40*self.app.height/100
        x = self.app.width/2
        w,h = self.app.width/3,self.bigButtonHeight
        font = f"Helvetica {int(self.app.width/30)} bold"
        fill = "light blue"
        self.scaleButton = Button(x,y,w,h,font,fill)
        x = (50+35)*self.app.width/100
        w,h = self.app.width/10,self.app.height/10
        text = "-->"
        font = f"Helvetica {int(self.app.width/50)} bold"
        fill = "blue"
        self.changeScaleButton = Button(x,y,w,h,font,fill)

    
    def makeLabelsOnButton(self):
        y = 60*self.app.height/100
        x = self.app.width/2
        w,h = self.app.width/3,self.bigButtonHeight
        font = f"Helvetica {int(self.app.width/30)} bold"
        fill = "light blue"
        self.labelsOnButton = Button(x,y,w,h,font,fill)
        x = (50+35)*self.app.width/100
        w,h = self.app.width/10,self.app.height/10
        text = "-->"
        font = f"Helvetica {int(self.app.width/50)} bold"
        fill = "blue"
        self.changeLabelsButton = Button(x,y,w,h,font,fill)

    def makeSpeedButton(self):
        y = 80*self.app.height/100
        x = self.app.width/2
        w,h = 44*self.app.width/100,self.bigButtonHeight
        font = f"Helvetica {int(self.app.width/30)} bold"
        fill = "light blue"
        self.speedButton = Button(x,y,w,h,font,fill)

        x = (50+35)*self.app.width/100
        w,h = self.app.width/10,self.app.height/10
        text = "+"
        font = f"Helvetica {int(self.app.width/50)} bold"
        fill = "blue"
        self.speedPlusButton = Button(x,y,w,h,font,fill)

        x = (50-35)*self.app.width/100
        text = "-"
        self.speedMinusButton = Button(x,y,w,h,font,fill)

   
    
    def redrawAll(self,canvas):
        # canvas.create_image(self.app.width/2,self.app.height/2, image=ImageTk.PhotoImage(self.background))
        canvas.create_text(self.app.width/2,self.app.height/15,text="Settings:",font="Helvetica 50 bold")
        canvas.create_text(self.app.width/2,19*self.app.height/20,text=f"(click {self.buttonToGameMode} to continue)")

        canvas.create_rectangle(self.dBetweenButton.x1,self.dBetweenButton.y1,self.dBetweenButton.x2,self.dBetweenButton.y2,fill=self.dBetweenButton.fill)
        canvas.create_text(self.dBetweenButton.x,self.dBetweenButton.y,text=f"Length Between Notes: {self.app.gameMode.difficulty}",font=self.dBetweenButton.font)

        canvas.create_rectangle(self.dBetweenPlusButton.x1,self.dBetweenPlusButton.y1,self.dBetweenPlusButton.x2,self.dBetweenPlusButton.y2,fill=self.dBetweenPlusButton.fill)
        canvas.create_text(self.dBetweenPlusButton.x,self.dBetweenPlusButton.y,text="+",font=self.dBetweenPlusButton.font)

        canvas.create_rectangle(self.dBetweenMinusButton.x1,self.dBetweenMinusButton.y1,self.dBetweenMinusButton.x2,self.dBetweenMinusButton.y2,fill=self.dBetweenMinusButton.fill)
        canvas.create_text(self.dBetweenMinusButton.x,self.dBetweenMinusButton.y,text="-",font=self.dBetweenMinusButton.font)

        canvas.create_rectangle(self.scaleButton.x1,self.scaleButton.y1,self.scaleButton.x2,self.scaleButton.y2,fill=self.scaleButton.fill)
        canvas.create_text(self.scaleButton.x,self.scaleButton.y,text=f"Scale: {self.app.gameMode.scaleName}",font=self.scaleButton.font)

        canvas.create_rectangle(self.changeScaleButton.x1,self.changeScaleButton.y1,self.changeScaleButton.x2,self.changeScaleButton.y2,fill=self.changeScaleButton.fill)
        canvas.create_text(self.changeScaleButton.x,self.changeScaleButton.y,text="-->",font=self.changeScaleButton.font)

        canvas.create_rectangle(self.labelsOnButton.x1,self.labelsOnButton.y1,self.labelsOnButton.x2,self.labelsOnButton.y2,fill=self.labelsOnButton.fill)
        canvas.create_text(self.labelsOnButton.x,self.labelsOnButton.y,text=f"Labels: {self.app.gameMode.labelsOn}",font=self.labelsOnButton.font)

        canvas.create_rectangle(self.changeLabelsButton.x1,self.changeLabelsButton.y1,self.changeLabelsButton.x2,self.changeLabelsButton.y2,fill=self.changeLabelsButton.fill)
        canvas.create_text(self.changeLabelsButton.x,self.changeLabelsButton.y,text="-->",font=self.changeLabelsButton.font)

        canvas.create_rectangle(self.speedButton.x1,self.speedButton.y1,self.speedButton.x2,self.speedButton.y2,fill=self.speedButton.fill)
        canvas.create_text(self.speedButton.x,self.speedButton.y,text=f"Speed Of Notes: {self.app.gameMode.ndx}",font=self.speedButton.font)

        canvas.create_rectangle(self.speedPlusButton.x1,self.speedPlusButton.y1,self.speedPlusButton.x2,self.speedPlusButton.y2,fill=self.speedPlusButton.fill)
        canvas.create_text(self.speedPlusButton.x,self.speedPlusButton.y,text="+",font=self.speedPlusButton.font)

        canvas.create_rectangle(self.speedMinusButton.x1,self.speedMinusButton.y1,self.speedMinusButton.x2,self.speedMinusButton.y2,fill=self.speedMinusButton.fill)
        canvas.create_text(self.speedMinusButton.x,self.speedMinusButton.y,text="-",font=self.speedMinusButton.font)
    

    
    def keyPressed(self,event):
        if event.key == self.buttonToGameMode:      #"g"
            self.app.gameMode.timeBetweenNotes = self.app.gameMode.maxDifficulty - self.app.gameMode.difficulty       # edit this for speed of the notes
            self.app.setActiveMode(self.app.gameMode)


    def mousePressed(self,event):
        x1,y1,x2,y2 = self.dBetweenPlusButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            if self.app.gameMode.difficulty < self.app.gameMode.maxDifficulty-2:
                self.app.gameMode.difficulty += 1

        x1,y1,x2,y2 = self.dBetweenMinusButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            if self.app.gameMode.difficulty > 1:
                self.app.gameMode.difficulty -= 1

        x1,y1,x2,y2 = self.changeScaleButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1: #TODO
            self.app.gameMode.scale = self.scales[self.i]
            self.i += 1
            self.i %= len(self.scales)
            self.app.gameMode.getScaleName()
            self.app.gameMode.getScaleFlatIndicators()
            self.app.gameMode.scaleNums = [num for num in self.app.gameMode.scale]
            self.app.gameMode.scaleNumsCopy = sorted(self.app.gameMode.scaleNums[:])
            self.app.gameMode.scaleConverter = dict()        # keyNum
            for i in range(self.app.gameMode.numOfSpacesAndLines):
                self.app.gameMode.scaleConverter[i] = self.app.gameMode.scaleNumsCopy[0]
                self.app.gameMode.scaleNumsCopy.pop(0)

            # self.app.gameMode.pickRandomScale()

        x1,y1,x2,y2 = self.changeLabelsButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            if self.app.gameMode.labelsOn == "on":
                self.app.gameMode.labelsOn = "off"
            else:
                self.app.gameMode.labelsOn = "on"

        x1,y1,x2,y2 = self.speedPlusButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            self.app.gameMode.ndx += 1

        x1,y1,x2,y2 = self.speedMinusButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            if self.app.gameMode.ndx > 1:
                self.app.gameMode.ndx -= 1

        



# from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class MyModalApp(ModalApp):
    def appStarted(app):
        # app.titleScreenMode = TitleScreenMode()
        # app.instructionsMode = InstructionsMode()
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)
 
 
app = MyModalApp(width=1000, height=700)     # size of window can be changed here