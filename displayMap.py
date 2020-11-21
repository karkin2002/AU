import pygame, time, config, random
# import config

## Setup the background surface
def backgroundSurfaceSetup(mapArray,textureLayers,pixelChange,chunkSize,mapHeight,mapWidth):
    backgroundSurface = pygame.Surface((len(mapArray[0])*chunkSize,len(mapArray)*chunkSize), pygame. SRCALPHA) # Creates a surface for the ground textures to sit on
    
    px = 0
    py = 0

    ## Iterates through each chunk on the map 
    ## and blips it to the background surface
    config.loadingNum = 0
    numY = 0
    for y in mapArray:
        numX = 0
        for x in y:
            chunkPosX = px+(numX*chunkSize)
            chunkPosY = py+(numY*chunkSize)
            
            if x.groundLayer != None:
                backgroundSurface.blit(textureLayers.groundLayerDic[x.groundLayer],(chunkPosX,chunkPosY))
            
            if x.surfaceLayer != None:
                backgroundSurface.blit(textureLayers.surfaceLayerDic[x.surfaceLayer],(chunkPosX,chunkPosY))
            
            if x.objectLayer != None:
                backgroundSurface.blit(textureLayers.objectLayerDic[x.objectLayer],(chunkPosX,chunkPosY))     
       
            numX += 1
        config.loadingNum += 1
        numY += 1

    return backgroundSurface


## Recieves a texture and a location of the texture in the map array
## and calculates the position it would be at on the map pixel wise
## before bliting the texture to the background surface
def backgroundSurfaceUpdate(backgroundSurface,textureObj,objRow,mapArray,chunkSize,textureLayers):
    yPosInArray = mapArray.index(objRow)
    xPosInArray = objRow.index(textureObj)
    yPosInPixles = yPosInArray * chunkSize
    xPosInPixles = xPosInArray * chunkSize
    
    if textureObj.groundLayer != None:
        backgroundSurface.blit(textureLayers.groundLayerDic[textureObj.groundLayer],(xPosInPixles,yPosInPixles))
    else:
        pygame.draw.rect(backgroundSurface,(100,0,0),(xPosInPixles,yPosInPixles,chunkSize,chunkSize))
        
    if textureObj.surfaceLayer != None:
        backgroundSurface.blit(textureLayers.surfaceLayerDic[textureObj.surfaceLayer],(xPosInPixles,yPosInPixles))
    
    if textureObj.objectLayer != None:
        backgroundSurface.blit(textureLayers.objectLayerDic[textureObj.objectLayer],(xPosInPixles,yPosInPixles))
    


def spaceBackdrop(win,pixelChange,starNum):
    
    spaceSurface = pygame.Surface((win.get_width()*2,win.get_height()*2), pygame. SRCALPHA)
    
    for _ in range (int(starNum*pixelChange)):
        pygame.draw.rect(spaceSurface,(255,255,255),(random.randint(0,spaceSurface.get_width()),random.randint(0,spaceSurface.get_height()),int(2*pixelChange),int(2*pixelChange)))
    
    spaceSurfaceX = -(spaceSurface.get_width()/4)
    
    spaceSurfaceY = -(spaceSurface.get_height()/4)

    return spaceSurface, spaceSurfaceX, spaceSurfaceY