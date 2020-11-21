import pygame

## Class used for the camera player movement
class camera:
    def __init__(self,pixelChange,win,width,height):
        self.width = int(width * pixelChange)
        self.height = int(height * pixelChange)
        self.x = win.get_width() / 2 - self.width / 2
        self.y = win.get_height() / 2 - self.height / 2
        self.collisionRect = pygame.Rect(self.x,self.y,self.width,self.height)
    
    def drawCollision(self,win):
        pygame.draw.rect(win,(200,100,100),(self.x,self.y,self.collisionRect.width,self.collisionRect.height),2)
