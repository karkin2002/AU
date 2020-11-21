import pygame

def loadImage(chunkSize,image,amount = 0): # Loading images that don't need rotation
    textureList = []
    if amount > 0:
        for i in range(1,amount+1):
            textureList.append(pygame.image.load(f'data/images/textures/player/{image}{i}.png')) # Loading the image into memory
            textureList[i-1] = pygame.transform.scale(textureList[i-1],(chunkSize,chunkSize)) # Scaling the images to the correct chunk size
    else:
        textureList.append(pygame.image.load(f'data/images/textures/player/{image}.png'))
        textureList[0] = pygame.transform.scale(textureList[0],(chunkSize,chunkSize))
    
    return textureList


class player:
    def __init__(self,chunkSize):
        ## Assigning and loading players animation
        self.playerAnimationDic = {
            "right":[],
            "left":[],
            "up":[],
            "down":[]
        }

        for i in self.playerAnimationDic:
            self.playerAnimationDic[i] = loadImage(chunkSize,i,3)