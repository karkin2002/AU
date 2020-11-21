import pygame
from imageSearch import findTextures
from printTerminal import printTerminal
from textCreator import createText

## Class used to store the player data
class player:
    def __init__(self,chunkSize,pixelChange,x,y,width,height,playerTextureDir):
        self.gridRef = [0,0]
        self.x = x
        self.y = y - chunkSize/2
        self.width = width
        self.height = height
        self.playerRect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.playerCollisionRect = pygame.Rect(self.x,self.y,self.width,2) # Rect used for collision detection
        self.collisions = []
        
        self.inventory = []

        ## Player Stats
        self.health = 0
        self.hunger = 0
        self.fatigue = 0
        self.disease = 0
        self.intelligence = 0
        self.strength = 0
        self.luck = 0
        self.charisma = 0
        self.happiness = 0
        self.anxiety = 0
        self.agility = 0
        self.science = 0
        self.race = None
        self.gender = None



        ## Works out the number of animations needed for each direction
        ## and splits them into 4 lists for each direction
        animationList = findTextures(playerTextureDir)
        
        animationNum = 0
        animationTotal = len(animationList)/4


        self.animationList = []

        directionAnimationList = []
        for eachImage in animationList:
            
            tempImage = pygame.image.load(eachImage)
            directionAnimationList.append(pygame.transform.scale(tempImage,(width,height)))


            if animationNum+1 == animationTotal:
                animationNum = 0
                self.animationList.append(directionAnimationList)
                directionAnimationList = []
            else:
                animationNum += 1
            

        
        self.position = self.animationList[0][0]
        self.direction = "down"
        self.walkCount = 0
        self.lastPosition = self.position

        self.animationMax = 32
        self.animationSpeed = 8


    def checkCollisions(self,win,changeX,changeY):
        self.playerCollisionRect = pygame.Rect(self.x+changeX,(self.y+self.height)+changeY,self.playerCollisionRect.width,3)
        # pygame.draw.rect(win,(0,0,0),(playerCollideRect.x,playerCollideRect.y,playerCollideRect.width,playerCollideRect.height))
        for i in self.collisions:
            if self.playerCollisionRect.colliderect(i):
                # pygame.draw.rect(win,(255,255,255),(i.x,i.y,i.width,i.height),5)
                return True
        
        return False



    def addCollision(self,win,chunkSize,mapX,mapY,gridRefX,gridRefY,mapArray):
        if mapArray[gridRefY][gridRefX].collision == True:
            # pygame.draw.rect(win,(100,100,100),((gridRefX)*chunkSize+mapX,(gridRefY)*chunkSize+mapY,chunkSize,chunkSize),1)
            self.collisions.append(pygame.Rect((gridRefX)*chunkSize+mapX,(gridRefY)*chunkSize+mapY,chunkSize,chunkSize))





    ## Updates the grid around the player
    def updateGridRef(self,win,chunkSize,mapX,mapY,mapArray):
        self.gridRef = [int(((self.x+self.width/2)-mapX)/chunkSize),int(((self.y+self.height)-mapY)/chunkSize)] # Get's the grid coordintes of the player
        
        ## Works out what grids around the player have collisions
        self.collisions = []

        if self.gridRef[0] > 0:
            self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0]-1,self.gridRef[1],mapArray)
            if self.gridRef[1] > 0:
                self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0]-1,self.gridRef[1]-1,mapArray)
            
            if self.gridRef[1] < len(mapArray)-1:
                self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0]-1,self.gridRef[1]+1,mapArray)
        
        if self.gridRef[0] < len(mapArray[0])-1:
            self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0]+1,self.gridRef[1],mapArray)

            if self.gridRef[1] > 0:
                self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0]+1,self.gridRef[1]-1,mapArray)

            if self.gridRef[1] < len(mapArray)-1:
                self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0]+1,self.gridRef[1]+1,mapArray)
        
        if self.gridRef[1] > 0:
            self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0],self.gridRef[1]-1,mapArray)
        
        if self.gridRef[1] < len(mapArray)-1:
            self.addCollision(win,chunkSize,mapX,mapY,self.gridRef[0],self.gridRef[1]+1,mapArray)


    ## Moves the player
    def move(self,dt):
        if self.walkCount + 1 >= self.animationMax:
            self.walkCount = 0
        
        if self.direction == "up":
            self.lastPosition = self.animationList[3][0]
            self.position = self.animationList[3][int(self.walkCount)//self.animationSpeed]
            self.walkCount += 1 * dt
            
        elif self.direction == "down":
            self.lastPosition = self.animationList[0][0]
            self.position = self.animationList[0][int(self.walkCount)//self.animationSpeed]
            self.walkCount += 1 * dt

        elif self.direction == "right":
            self.lastPosition = self.animationList[2][0]
            self.position = self.animationList[2][int(self.walkCount)//self.animationSpeed]
            self.walkCount += 1 * dt

        elif self.direction == "left":
            self.lastPosition = self.animationList[1][0]
            self.position = self.animationList[1][int(self.walkCount)//self.animationSpeed]
            self.walkCount += 1 * dt
        
        else:
            self.position = self.lastPosition

    def drawPlayer(self,win):
        win.blit(self.position,(self.x,self.y))
        
    def drawCollision(self,win,mapX,mapY,chunkSize):
        pygame.draw.rect(win,(100,100,200),(self.gridRef[0]*chunkSize+mapX,self.gridRef[1]*chunkSize+mapY,chunkSize,chunkSize),1)
        pygame.draw.rect(win,(200,100,100),(self.x,self.y,self.playerRect.width,self.playerRect.height),1)
    

class staticEntity:
    def __init__(self,win,pixelChange,chunkDifference,x,y,width,height,flowerAnimationDir,animationMax,animationSpeed):
        self.x = (x * pixelChange) * chunkDifference
        self.y = (y * pixelChange) * chunkDifference
        self.width = width
        self.height = height

        self.collisionRect = pygame.Rect(x,y,width,height)
        
        flowerAnimationFiles = findTextures(flowerAnimationDir)
        textBoxAnimationFiles = findTextures("data/images/textures/entity/flowerText/")

        self.animationList = []
        for eachImage in flowerAnimationFiles:
            
            tempImage = pygame.image.load(eachImage)
            self.animationList.append(pygame.transform.scale(tempImage,(width,height)))

        self.textBoxAnimationList = []
        for eachImage in textBoxAnimationFiles:
            
            tempImage = pygame.image.load(eachImage)
            self.textBoxAnimationList.append(pygame.transform.scale(tempImage,(int(30*chunkDifference),int(31.4285714*chunkDifference))))


        self.position = self.animationList[0]
        self.direction = "down"
        self.walkCount = 0
        self.lastPosition = self.position

        self.animationMax = animationMax
        self.animationSpeed = animationSpeed
        self.textBoxOutline = pygame.Rect(win.get_width()/2-(1000*pixelChange)/2,(20*pixelChange),(1000*pixelChange),(250*pixelChange))
        self.textBox = pygame.Rect(win.get_width()/2-(980*pixelChange)/2,(30*pixelChange),(980*pixelChange),(230*pixelChange))

        self.astric = createText(win,"*","mvboli",(255,255,255),60)

        self.textBoxMessage = [["Howdy!"],["Howdy!","I'm FLOWEY"],["Howdy!","I'm FLOWEY","FLOWEY the FLOWER!"],["Hee hee hee"],["Why'd you make me introduce","myself?"],["It's rude to act like you don't","know who I am"],["Someone ought to teach you","proper manners"],["Anyway"],["Someone came through here","looking for you"],["Someone came through here","looking for you","They may have a surprise!"],["Go on through!"],["Go on through!","I'm sure we'll meet again"]]
        numY = 0
        for eachTextBox in self.textBoxMessage:#
            numX = 0
            for eachText in eachTextBox:
                self.textBoxMessage[numY][numX] = createText(win,eachText,"mvboli",(255,255,255),40)
                numX += 1
            numY += 1
        
        self.textBoxMessageNum = 0



    ## Moves the player
    def move(self,dt):

        if self.walkCount + 1 >= self.animationMax:
            self.walkCount = 0

        elif self.direction == "talking":
            self.lastPosition = self.animationList[0]
            self.position = self.animationList[int(self.walkCount)//self.animationSpeed]
            self.walkCount += 1 * dt
        
        else:
            self.position = self.lastPosition
            

    def draw(self,win,mapX,mapY):
        win.blit(self.position,(self.x+mapX,self.y+mapY))

    def displayText(self,win,dt):
        pygame.draw.rect(win,(255,255,255),self.textBoxOutline)
        pygame.draw.rect(win,(0,0,0),self.textBox)
        
        if self.textBoxMessageNum < len(self.textBoxMessage):
            y = 40
            for eachText in self.textBoxMessage[self.textBoxMessageNum]:
                try:
                    if eachText != self.textBoxMessage[4][1] and eachText != self.textBoxMessage[5][1] and eachText != self.textBoxMessage[6][1]  and eachText != self.textBoxMessage[8][1]  and eachText != self.textBoxMessage[9][1]:
                        win.blit(self.astric,(720,y-5))
                except:
                    win.blit(self.astric,(720,y-5))
                win.blit(eachText,(760,y))
                y += 70

        win.blit(self.textBoxAnimationList[int(self.walkCount)//self.animationSpeed],(500,50))

        