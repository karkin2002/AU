
## Class used to save the games data
class gameData:
    def __init__(self,resolution,fullscreen,framerate,alpha,FPS,gridRef):
        self.gridRef = gridRef
        self.velocity = 4.5
    
        self.resolution = resolution
        self.fullscreen = fullscreen
        self.framerate = framerate
        self.alpha = alpha
        self.FPS = FPS

        ## Value states whether the player is playing the game or in menus
        self.inGame = True

