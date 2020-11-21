import pickle
from gameData import gameData
from printTerminal import *
from chunkClass import chunk

def createNewSave(filename,resolution,fullscreen,framerate,alpha,FPS,gridRef=[0,0]):
    with open(filename, 'wb') as output:

        obj = gameData(resolution,fullscreen,framerate,alpha,FPS,gridRef)
        
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        printTerminal("Info",f"Created new save '{filename}'")

    
    return obj



def loadSave(filename,resolution=5,fullscreen=False,framerate=60,alpha=True,FPS=False,gridRef=[0,0]):
    try:
        with open(filename, 'rb') as input:
            save = pickle.load(input)
            printTerminal("Info",f"Loaded save '{filename}'")
    
    except:
        save = createNewSave(filename,resolution,fullscreen,framerate,alpha,FPS,gridRef)
        printTerminal("Info",f"Cannot load save '{filename}'")
    
    return save



def saveGame(filename, obj):
    try:
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
            printTerminal("Info",f"Saved '{filename}'")
    
    except:
        printTerminal("Info",f"Cannot save '{filename}'")



def saveMap(mapName,mapArray,gridRef=[0,0]):
    mapArrayTxt = open(f"data/saves/{mapName}.txt", "w")
    mapArrayString = ""
    
    numY = 0
    for eachRow in mapArray:
        numX = 0
        for eachItem in eachRow:
            if len(mapArray[0])-1 > numX:
                mapArrayString += f"{eachItem.groundLayer},{eachItem.surfaceLayer},{eachItem.objectLayer},{eachItem.collision}|"
            else:
                mapArrayString += f"{eachItem.groundLayer},{eachItem.surfaceLayer},{eachItem.objectLayer},{eachItem.collision}"
            numX += 1
        
        if len(mapArray)-1 > numY: 
            mapArrayString += "\n"

        numY += 1

    mapArrayTxt.write(f"{mapArrayString}")
    mapArrayTxt.close()

    mapDataTxt = open(f"data/saves/{mapName}Data.txt", "w")
    mapDataTxt.write(f"{gridRef[0]},{gridRef[1]}")
    mapDataTxt.close()