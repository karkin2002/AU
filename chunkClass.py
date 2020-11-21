class chunk:
    
    ## Class used for each chunk in the map array
    def __init__(self,groundLayer = None,surfaceLayer = None,objectLayer = None,collision = False):
        self.groundLayer = groundLayer
        self.surfaceLayer = surfaceLayer
        self.objectLayer = objectLayer
        self.collision = collision
