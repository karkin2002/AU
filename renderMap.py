import pygame
from displayMap import backgroundSurfaceUpdate
from particleSystem import *


def renderMap(win,mapArray,chunkSize,textureLayers,pixelChange,px,py,mousePos,mousePress,place,inGame,creative,backgroundSurface,mapHeight,mapWidth,dt,clickCounter):

    win.blit(backgroundSurface,(px,py))

    if creative == True and mousePress[0] == True and inGame == True:
        renderDistance = 1
        
        numY = 0
        for y in mapArray:

            numX = 0
            for x in y:
                chunkPosX = px+(numX*chunkSize) 
                chunkPosY = py+(numY*chunkSize)
                
                if (chunkPosX < win.get_width()+(renderDistance*chunkSize) and chunkPosX > 0-(renderDistance*chunkSize)) and (chunkPosY < win.get_height()+(renderDistance*chunkSize)  and chunkPosY > 0-(renderDistance*chunkSize)):
                    rect1 = pygame.Rect(chunkPosX,chunkPosY,chunkSize,chunkSize)

                        
                    
                    if rect1.collidepoint(mousePos):
                        
                        ## Placing ground
                        if place in textureLayers.groundLayerDic:
                            x.groundLayer = place
                        
                        ## Placing surface
                        elif place in textureLayers.surfaceLayerDic:
                            x.surfaceLayer = place

                        ## Placing object
                        elif place in textureLayers.objectLayerDic:
                            x.objectLayer = place

                        ## Deleting
                        else:
                            if place == "deleteGround":
                                x.groundLayer = None
                            
                            elif place == "deleteSurface":
                                x.surfaceLayer = None
                            
                            elif place == "particle" and clickCounter == 1:
                                textureLayers.particles.append(smokeParticleGroup(-0.04,1,(chunkPosX+chunkSize/2)-px,(chunkPosY+chunkSize/2)-py))

                            elif place == "collision":
                                x.collision = True
                            
                            elif place == "deleteCollision":
                                x.collision = False
                            
                            else:
                                x.objectLayer = None
                    
                        
                        backgroundSurfaceUpdate(backgroundSurface,x,y,mapArray,chunkSize,textureLayers)


                numX += 1
            numY += 1

    for i in textureLayers.particles:
        i.updateParicles(win,dt,pixelChange,px,py)
        
    
    return backgroundSurface, mapArray


    




