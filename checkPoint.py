import pygame
from player import player

## Superclass for checkpoints
class checkPoint:
    def __init__(self,x,y,width,height,pixelChange,playerChunkDifference):
        self.staticX = (x * pixelChange)*playerChunkDifference
        self.staticY = (y* pixelChange)*playerChunkDifference
        self.x = self.staticX
        self.y = self.staticY
        self.width = (width * pixelChange)*playerChunkDifference
        self.height = (height * pixelChange)*playerChunkDifference
        self.collisionRect = pygame.Rect(self.x,self.y,self.width,self.height)

    ## Draws the checkpoint on a surface
    def draw(self,surf):
        pygame.draw.rect(surf,(255,0,0),pygame.Rect(self.x,self.y,self.width,self.height),1)
    
    ## Updates the position of the rect used for collision
    def updateCollisionRect(self):
        self.collisionRect = pygame.Rect(self.x,self.y,self.width,self.height)
    
    def update(self,mapX,mapY):
        self.x = self.staticX + mapX
        self.y = self.staticY + mapY
        self.updateCollisionRect()

    ## Returns whether there is a collsion with the plater
    def checkCollision(self,playerRect):
        return self.collisionRect.colliderect(playerRect)




## Check Point used to load new map
class loadMapCheckPoint(checkPoint):
    def __init__(self,x,y,width,height,pixelChange,playerChunkDifference,mapNameFrom,mapNameTo,location=None):
        super().__init__(x,y,width,height,pixelChange,playerChunkDifference)
        self.mapNameFrom = mapNameFrom # Stores the name of the Map the check point is in
        self.mapNameTo = mapNameTo # Stores the name of the Map the check point sends the player to
        self.location = location # The location it sends the player



class booleanCheckPoint(checkPoint):
    def __init__(self,x,y,width,height,pixelChange,playerChunkDifference,mapNameFrom):
        super().__init__(x,y,width,height,pixelChange,playerChunkDifference)
        self.trigger = False
        self.mapNameFrom = mapNameFrom
    
    def checkCollision(self,playerRect):
        self.trigger = self.collisionRect.colliderect(playerRect)




class teleportCheckPoint(checkPoint):
    def __init__(self,x,y,width,height,pixelChange,playerChunkDifference,gridRef):
        super().__init__(x,y,width,height,pixelChange,playerChunkDifference)
        self.gridRef = gridRef
    
    def checkCollision(self,playerRect):
        return self.collisionRect.colliderect(playerRect)

    def teleportPlayer(self,win,player,mapX,mapY,chunkSize):
        if self.checkCollision(player.playerCollisionRect):
            mapX = win.get_width() / 2
            mapY = win.get_height() / 2
            mapX -= self.gridRef[0]*chunkSize
            mapY -= (self.gridRef[1]-1)*chunkSize
            player.x = mapX + self.gridRef[0]*chunkSize
            player.y = mapY + (self.gridRef[1]-1)*chunkSize

        return mapX, mapY, player
