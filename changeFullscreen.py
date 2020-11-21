import pygame
from inGameMenu import inGameMenuSetUp
from setup import *

## Sets the win to be fullscreen or windowed depending on arguments
def changeFullscreen(win,fullscreen):

    if fullscreen:
        win = pygame.display.set_mode((win.get_width(),win.get_height()), pygame.DOUBLEBUF | pygame.FULLSCREEN)

    else:
        win = pygame.display.set_mode((win.get_width(),win.get_height()), pygame.DOUBLEBUF)

## Resizes all the images and text according to the screen size
def resize(win,alpha,mapWidth,mapHeight,chunkSize,chunkScaleNum):
    mapWidth, mapHeight, chunkSize, renderDistance, pixelChange = sizeSetup(mapWidth,mapHeight,chunkScaleNum)
    textureDic = setupImages(chunkSize)
    menuSurface, menuRectCollisionDic, menuTextList = inGameMenuSetUp(win,alpha,pixelChange,chunkSize,textureDic)

    return mapWidth, mapHeight, chunkSize, renderDistance, pixelChange, textureDic, menuSurface, menuRectCollisionDic, menuTextList


## Used for changing the resolution on the main menu
def changeResolution(win,fullscreen,resolution,resolutionList):
    ## Takes the resolution you want from the list
    ## removes the x in the middle and splits it into
    ## a winow width and window height
    resolution = resolutionList[resolution]
    resolution = resolution.split("×") # Not an 'x' it is a special character '×'
    winWidth = int(resolution[0])
    winHeight = int(resolution[1])

    ## Setting the window to the new size
    if fullscreen:
        win = pygame.display.set_mode((winWidth,winHeight), pygame.DOUBLEBUF | pygame.FULLSCREEN)

    else:
        win = pygame.display.set_mode((winWidth,winHeight), pygame.DOUBLEBUF)
