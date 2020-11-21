import pygame, time, random
from cellularAutomata import *
from chunkClass import *
from displayMap import backgroundSurfaceSetup
from printTerminal import *
from saving import *
from layers import layer
from printTerminal import printTerminal
from imageSearch import *
from readingTextfiles import openMapArray
import config





def setupDisplay(winWidth, winHeight, fullscreen,name = "Project Arctic"): # Setting up the window
    
    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h] # Recieves resolution of monitor
    
    if fullscreen == False:
        win = pygame.display.set_mode((winWidth, winHeight),pygame.DOUBLEBUF) # Windowed mode
    else:
        win = pygame.display.set_mode((winWidth,winHeight), pygame.DOUBLEBUF | pygame.FULLSCREEN) # Fullscreen mode
    
    pygame.display.set_caption(name)

    return win, monitor_size



def setupTime(): # Set up timings
    clock = pygame.time.Clock() # Seting put clock
    last_time = time.time() # Used for delta time

    return clock, last_time



def mapSetup(mapHeight,mapWidth,chunkSize,randomWorld): # Creating a new map array

    num = 1
    groundMapArray = []
    textureChoice = ["data/images/textures/groundLayer\grass1.png","data/images/textures/groundLayer\grass2.png","data/images/textures/groundLayer\grass3.png","data/images/textures/groundLayer\grass4.png"]
    
    for _ in range(mapHeight//chunkSize):
        widthMapLayout = []
        
        for _ in range(mapWidth//chunkSize):

            texture = textureChoice[0]

            if randomWorld == True:
                texture = random.choice(textureChoice)
            
            widthMapLayout.append((chunk(texture)))
        
        config.loadingNum = num
        
        num += 1
        groundMapArray.append(widthMapLayout)

    # groundMapArray = cellularAutomata(groundMapArray,7)
    return groundMapArray



def sizeSetup(win,mapWidth,mapHeight,chunkScaleNum):
    pixelChange = win.get_width() / 1920
    chunkSize = int((16*(chunkScaleNum+1))* pixelChange)# The size of each chunk texture in pixels
    mapWidth *= chunkSize # Converting the chunks into pixels
    mapHeight *= chunkSize
    return mapWidth, mapHeight, chunkSize, pixelChange




### ------  Textures  ------ ###

def loadImage(chunkSize,dic,directory): # Loading images that don't need rotation
    
    textureFileList = findTextures(directory)
    
    for eachImage in textureFileList:
        try:
            dic[eachImage] = pygame.image.load(eachImage)
            dic[eachImage] = pygame.transform.scale(dic[f"{eachImage}"],(chunkSize,chunkSize))
        
        except:
            ## If the texture can't load replace it with the error texture
            printTerminal("ERROR",f"Couldn't load image {eachImage}")
            dic[f"{eachImage}"] = pygame.image.load(eachImage)
            dic[f"{eachImage}"] = pygame.transform.scale(dic[f"{eachImage}"],(chunkSize,chunkSize))


    return dic


def setupImages(chunkSize): # Setting up all the images
    textureLayers = layer()

    textureLayers.groundLayerDic = loadImage(chunkSize,textureLayers.groundLayerDic,"data/images/textures/groundLayer/")
    textureLayers.surfaceLayerDic = loadImage(chunkSize,textureLayers.surfaceLayerDic,"data/images/textures/surfaceLayer/")
    textureLayers.objectLayerDic = loadImage(chunkSize,textureLayers.objectLayerDic,"data/images/textures/objectLayer/")

    return textureLayers



# ## ------  Setup  ------ ##
def setup(argsList):
    # try:
    win = argsList[0]
    newSave = argsList[1]
    resolution = argsList[2]
    fullscreen = argsList[3]
    framerate = argsList[4]
    mapWidth = argsList[5]
    mapHeight = argsList[6]
    alpha = argsList[7]
    FPS = argsList[8]
    randomWorld = argsList[9]
    chunkScaleNum = argsList[10]
    mapName = argsList[11]

    config.stage = 1
    clock, last_time = setupTime()

    config.stage = 2
    # Loading players and animals

    config.stage = 3
    mapWidth, mapHeight, chunkSize, pixelChange = sizeSetup(win,mapWidth,mapHeight,chunkScaleNum)

    config.stage = 4
    textureLayers = setupImages(chunkSize)


    if newSave == True:
        config.stage = 5
        groundMapArray =  mapSetup(mapHeight,mapWidth,chunkSize,randomWorld)

        saveMap(mapName,groundMapArray)

        config.stage = 6
        game = createNewSave("data/saves/gameData.pkl",resolution,fullscreen,framerate,alpha,FPS)

        gridRef = [0,0]


    else:
        config.stage = 7
        
        game = loadSave("data/saves/gameData.pkl")

        groundMapArray, gridRef = openMapArray(mapName)
        
    config.stage = 8
    backgroundSurface = backgroundSurfaceSetup(groundMapArray,textureLayers,pixelChange,chunkSize,mapHeight,mapWidth)
            

    config.stage = 9

    config.loadingRun = False
    return clock, last_time, mapWidth, mapHeight, chunkSize, pixelChange, textureLayers, game, backgroundSurface, groundMapArray, gridRef
    # except Exception as e: printTerminal("ERROR",f"Startup thread '{e}'")