import pygame
from textCreator import *
from changeFullscreen import *

def changeFullscreen(win,fullscreen):

    if fullscreen:
        win = pygame.display.set_mode((win.get_width(),win.get_height()), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)

    else:
        win = pygame.display.set_mode((win.get_width(),win.get_height()), pygame.HWSURFACE | pygame.DOUBLEBUF)

def checkBoxFullscreen(win,value,rect,mousePress,mousePos,clickCounter,pixelChange):
    if mousePress[0] == True and rect.collidepoint(mousePos) and clickCounter == 1:
        value = not value
        changeFullscreen(win,value)
    
    if value == True:
        pygame.draw.rect(win, (100,200,100), rect)
        pygame.draw.rect(win, (0,0,0), rect,int(3*pixelChange))
        
    else:
        pygame.draw.rect(win, (200,100,100), rect)
        pygame.draw.rect(win, (0,0,0), rect,int(3*pixelChange))
        

    return value



def checkBox(win,value,rect,mousePress,mousePos,clickCounter,pixelChange):
    if mousePress[0] == True and rect.collidepoint(mousePos) and clickCounter == 1:
        value = not value
    
    if value == True:
        pygame.draw.rect(win, (100,200,100), rect)
        pygame.draw.rect(win, (0,0,0), rect,int(3*pixelChange))
        
    else:
        pygame.draw.rect(win, (200,100,100), rect)
        pygame.draw.rect(win, (0,0,0), rect,int(3*pixelChange))
        

    return value



class slider:
    def __init__(self,pixelChange,x,y,width,height,buttonWidth,buttonHeight,value,maxValue,sliderSurfaceColour = (100,100,100),buttonColour = (200,200,200)):
        self.maxValue = maxValue

        self.x = x * pixelChange
        self.y = y * pixelChange
        
        self.width = int(width * pixelChange)
        self.height = int(height * pixelChange)
        
        self.buttonWidth = int(buttonWidth * pixelChange)
        self.buttonHeight = int(buttonHeight * pixelChange)

        self.buttonX = (self.x - self.buttonWidth/2) + (value / maxValue)*self.width
        self.buttonY = self.y+(self.height/2 - self.buttonHeight / 2)
        
        self.sliderSurface = pygame.Surface((self.width+self.buttonWidth*2,self.height))
        self.sliderSurface.fill(sliderSurfaceColour)
        self.sliderRect = pygame.Rect(self.x-self.buttonWidth,self.y,self.width+self.buttonWidth*2,self.height)
        self.buttonRect = pygame.Rect(self.buttonX,self.buttonY,self.buttonWidth,self.buttonHeight)

        self.buttonColour = buttonColour



    def displaySlider(self,win):
        win.blit(self.sliderSurface,(self.x-self.buttonWidth,self.y))
        pygame.draw.rect(win,self.buttonColour,self.buttonRect)

    def updateSlider(self,win,mousePos,mousePress,pixelChange,value):
        value = (((self.buttonRect.x+self.buttonRect.width/2) - self.x)/pixelChange)/(self.width/pixelChange)

        if mousePress[0] == True and self.sliderRect.collidepoint(mousePos):
            
            if mousePos[0] > self.x and mousePos[0] <= self.x + self.width:
                self.buttonRect.x = mousePos[0] - self.buttonRect.width//2
            else:
                if mousePos[0] < self.x:
                    value = 0
                else:
                    value = 1

        self.displaySlider(win)

        value = int(value*self.maxValue)

        if pixelChange != 1.0:
            value += 1
            
            if value > self.maxValue:
                value = self.maxValue
            
            if value < 0:
                value = 0

        return value

    def displayText(self,win,pixelChange,value,font,colour,size):
        text = createText(win,str(value),font,colour,int(size*pixelChange))
        win.blit(text,(self.x+self.width+(50*pixelChange),self.y))



class textButton:
    def __init__(self,win,surf,pixelChange,text,font,colour,size,x,y):
        ButtonText = createText(win,text,font,colour,int(size * pixelChange))
        surf.blit(ButtonText,(x,y))

        self.Button = pygame.Rect(x,y,ButtonText.get_width(),ButtonText.get_height())

    def backButtonCollision(self,mousePress,mousePos,clickCounter):
        return mousePress[0] == True and self.Button.collidepoint(mousePos) and clickCounter == 1



class colourButton:
    def __init__(self,pixelChange,x,y,width,height,colour,edge = 0):
        self.x = x * pixelChange
        self.y = y * pixelChange
        self.width = int(width * pixelChange)
        self.height = int(height * pixelChange)
        self.edge = int(edge * pixelChange)
        self.colour = colour
        self.buttonRect = pygame.Rect(self.x,self.y,self.width,self.height)

    def displayButton(self,surf,pixelChange):
        pygame.draw.rect(surf, self.colour, self.buttonRect)
        
        if self.edge > 0:
            pygame.draw.rect(surf, (0,0,0), self.buttonRect, self.edge)

    def collision(self,mousePos,mousePress,clickCounter):
        if mousePress[0] == True and clickCounter == 1:
            return self.buttonRect.collidepoint(mousePos)

        else:
            return False
