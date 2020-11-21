import pygame, random, time


##  ------ Particle Super Classes ------  ##

## Particle Superclass
class particle:
    def __init__(self,x,y,accX,accY,height,width,colour,radius = None, alpha = None):
        self.x = x
        self.y = y

        self.accX = accX
        self.accY = accY

        self.radius = radius
        self.height = height
        self.width = width

        self.colour = colour

        self.aplha = alpha

        self.remove = False

## Particle Group Superclass
class particleGroup: 
    def __init__(self,accY,newParticleRate):
        self.particleDic = {}
        self.particleNum = 0
        self.particleRemoveList= []
        self.gravity = accY
        self.newParticleRate = newParticleRate
        self.newParticleNum = 0

    
    ## removes unwanted particles
    def removeParticles(self):
        for i in self.particleRemoveList:
            del self.particleDic[i]

        self.particleRemoveList = []




##  ------ Rain ------  ##

class rain(particle):
    def __init__(self,x,y,accX,accY,height,width,colour):
        super().__init__(x,y,accX,accY,height,width,colour)

    ## Drawing particle on the display
    def drawParticle(self,win,windX,pixelChange):
        pygame.draw.line(win,self.colour,(self.x, self.y),(self.x+windX, self.y+(self.height* pixelChange)),int(self.width* pixelChange))

    ## Moving particle
    def moveParticle(self,win,dt,windX,pixelChange):
        ## Particle Movement
        self.accX = windX
        self.x += (self.accX * dt) * pixelChange
        self.y += (self.accY * dt) * pixelChange
        
        ## Removes if height <= 0
        if self.height > 0:
            self.height -= (random.uniform(0.1,1.4) * dt)* pixelChange
        else:
            self.remove = True
        
        ## Removes if out of screen
        
        if self.y > win.get_height():
            self.remove = True



## Handles the particle as a group
class rainParticleGroup(particleGroup):
    def __init__(self,accY,newParticleRate):
        super().__init__(accY,newParticleRate)

    ## Adds new particle
    def newParticle(self,win,windX):
        height = 40
        self.particleDic[self.particleNum] = rain(random.randint(0-int(win.get_width()/4),int(win.get_width()+(win.get_width()/4))),0-height,0,random.randint(self.gravity-5,self.gravity+5),40,2,(175,195,204))
        self.particleNum += 1


    ## Updates all the particles within the particleDic
    def updateParicles(self,win,dt,windX,pixelChange):
        self.newParticleNum += self.newParticleRate  * dt

        if self.newParticleNum >= 100:
            for i in range(6):
                self.newParticle(win,windX)

            self.newParticleNum = 0

        for i in self.particleDic:
            self.particleDic[i].moveParticle(win,dt,windX,pixelChange)
            
            self.particleDic[i].drawParticle(win,windX,pixelChange)
            
            ## Adds any partices that need removing to a remove list
            if self.particleDic[i].remove == True:
                self.particleRemoveList.append(i)
        
        self.removeParticles()
    



##  ------ Vent Smoke ------  ##

class smoke(particle):
    def __init__(self,x,y,accX,accY,height,width,colour,radius):
        super().__init__(x,y,accX,accY,height,width,colour,radius)

    ## Drawing particle on the display
    def drawParticle(self,win,pixelChange,px,py):
        pygame.draw.circle(win,self.colour,(int(self.x+px), int(self.y+py)),int(self.radius* pixelChange))

    ## Moving particle
    def moveParticle(self,win,dt,pixelChange):
        ## Particle Movement
        self.x += (self.accX * dt) * pixelChange
        self.y += (self.accY * dt) * pixelChange

        self.accY += (0.0003 * dt)* pixelChange ## Change the rate at which the y accelerates

        
        ## Removes if height <= 0
        if self.radius > 0:
            self.radius -= (random.uniform(0.05,0.1) * dt)* pixelChange ## Change the rate of the radius chaning
        else:
            self.remove = True
        
        ## Removes if out of screen
        # if self.y > win.get_height():
        #     self.remove = True


## Handles the particle as a group
class smokeParticleGroup(particleGroup):
    def __init__(self,accY,newParticleRate,x,y):
        super().__init__(accY,newParticleRate)
        self.x = x
        self.y = y

    ## Adds new particle
    def newParticle(self,win,x,y,pixelChange):
        self.particleDic[self.particleNum] = smoke(random.uniform((x-25*pixelChange),(x+25*pixelChange)),random.uniform((y-30*pixelChange),(y+25*pixelChange)),random.uniform((-0.1*pixelChange),(0.1*pixelChange)),self.gravity,0,0,(random.randint(240,255),random.randint(240,255),random.randint(240,255)),random.uniform(15*pixelChange,20*pixelChange))
        self.particleNum += 1


    ## Updates all the particles within the particleDic
    def updateParicles(self,win,dt,pixelChange,px,py):

        self.newParticleNum += self.newParticleRate  * dt

        if self.newParticleNum >= 1000:
            for i in range(25):
                self.newParticle(win,self.x,self.y,pixelChange)
            
            self.newParticleNum = 0


        for i in self.particleDic:
            self.particleDic[i].moveParticle(win,dt,pixelChange)
            
            self.particleDic[i].drawParticle(win,pixelChange,px,py)
            
            ## Adds any partices that need removing to a remove list
            if self.particleDic[i].remove == True:
                self.particleRemoveList.append(i)
        
        self.removeParticles()