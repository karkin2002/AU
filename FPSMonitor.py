import datetime
from textCreator import *

## Used to display FPS
def SetupFPS():
    
    sec = datetime.timedelta(seconds=1)
    
    frames = 0
    
    nextFPStime = datetime.datetime.today() + sec

    
    framesText = None # Used for displaying the FPS on the window
    
    return sec, frames, nextFPStime, framesText # Don't return framesText if not displaying on window

## Updates the FPS and displayed in terminal
def updateFPS(sec, frames, nextFPStime,displayInTerminal = False):
    
    frames += 1
    

    if nextFPStime <= datetime.datetime.today():
        
        if displayInTerminal == True:
            print(frames)
        
        
        frames = 0
        nextFPStime = datetime.datetime.today() + sec
    
    return frames, nextFPStime


## Updates the FPS and displays on screen
def updateFPSDisplay(sec, frames, nextFPStime, win, pixelChange, framesText):
    
    frames += 1
    

    if nextFPStime <= datetime.datetime.today() or framesText == None :
        
        
        framesText = createText(win,f"FPS: {frames}","bahnschrift",(255,255,255),int(20 * pixelChange))
        
        frames = 0
        nextFPStime = datetime.datetime.today() + sec
    
    win.blit(framesText,(10,3))
    
    return frames, nextFPStime, framesText