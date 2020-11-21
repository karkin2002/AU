
import pygame


## Fade class, used to fade the screen out and in
class fade:
    def __init__(self,win,colour=(255,255,255),startBlack = True):
        self.fadeSurface = pygame.Surface((win.get_width(),win.get_height()))
        self.fadeSurface.set_colorkey(colour)
        if startBlack == True:
            self.fadeSurface.set_alpha(255)
        else:
            self.fadeSurface.set_alpha(0)
        self.fading = False

    ## Fades the screen to black
    def fadeIn(self,speed,dt):
        self.fading = True
        if self.fadeSurface.get_alpha() < 255:
            self.fadeSurface.set_alpha(self.fadeSurface.get_alpha()+(speed*dt))
        else:
            self.fading = False
    
    ## Fades the screen from back
    def fadeOut(self,speed,dt):
        self.fading = True
        if self.fadeSurface.get_alpha() > 0:
            self.fadeSurface.set_alpha(self.fadeSurface.get_alpha()-(speed*dt))
        else:
            self.fading = False

    ## Draws the surface to the display
    def draw(self,surf):
        if self.fadeSurface.get_alpha() != 0:
            surf.blit(self.fadeSurface,(0,0))


    