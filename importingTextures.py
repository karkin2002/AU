import pygame
from tkinter import *
from tkinter.filedialog import askopenfilename

def importTexture(width,height,saveFilename):
    root = Tk()
    filename = askopenfilename(parent=root)
    root.destroy()
    textureSheet = pygame.image.load(filename)
    
    textureSurface = pygame.Surface((width,height), pygame. SRCALPHA)

    num = 0
    numY = 0
    for imageY in range(int(textureSheet.get_height()/height)):
        
        numX = 0
        for imageX in range(int(textureSheet.get_width()/width)):
            textureSurface = pygame.Surface((width,height), pygame. SRCALPHA)
            textureSurface.blit(textureSheet,(numX,numY))
            pygame.image.save(textureSurface,f"testImage/{saveFilename}{num}.png")
            numX -= width
            num += 1
        
        numY -= height

importTexture(20,20,"undertaleStairs")