import pygame

def createText(win,text,font,colour,size): # Create Text
    
    fontFormat = pygame.font.SysFont(font,size)

    message = fontFormat.render(text,True,colour)

    return message