import pygame
from player import player
from textCreator import createText
from layers import layer

## Initialises Inventory Window
class inventoryWindow:
    def __init__(self,win,pixelChange,alpha):
        self.width = 16 * pixelChange
        self.height =  9 * pixelChange
        self.finalWidth = self.width*100
        self.finalHeight = self.height*100
        self.innerWidth = self.width
        self.innerHeight = self.height
        self.textColour = (200,200,210)
        
        if alpha == True:
            self.inventorySurface = pygame.Surface((self.finalWidth,self.finalHeight))
            self.inventorySurface.set_colorkey((0,0,0))
            self.inventorySurface.set_alpha(200)
        else:
            self.inventorySurface = pygame.Surface((self.finalWidth,self.finalHeight),pygame.SRCALPHA)
        
        self.exeTitle = createText(win,">> C:\\Users\\Name\\InventoryOS> IMP.exe","consolas",self.textColour,int(25*pixelChange))

        self.selectIcon = createText(win,">>","consolas",(80,220,80),int(25*pixelChange))
        self.selectAnimationCount = 0
        self.selectAnimationMax = 32
        self.selectX = 0
        self.selectVelocityX = 40 * pixelChange

        self.lineDownString = createText(win,"|","consolas",self.textColour,int(25*pixelChange))

    def drawLineDown(self,win,pixelChange,x):
        y =  (196 * pixelChange) - self.selectVelocityX
        for _ in range(29):
            win.blit(self.lineDownString,(x * pixelChange,y))
            y += self.lineDownString.get_height()

    def drawItemInfo(self,surf,mainPlayer,textureLayers,pixelChange):
        if len(mainPlayer.inventory) > 0 and len(mainPlayer.inventory) > self.selectX:
            itemImage = pygame.transform.scale(textureLayers.objectLayerDic[mainPlayer.inventory[self.selectX][0][1]],(int(200* pixelChange),int(200* pixelChange)))
            surf.blit(itemImage,(900* pixelChange, 200 * pixelChange))

def openInventory(win,dt,inventory, mainPlayer,pixelChange,textureLayers):
    
    if inventory.selectX > len(mainPlayer.inventory):
        inventory.selectX = len(mainPlayer.inventory) -1 


    pygame.draw.rect(inventory.inventorySurface,(150,150,150),(inventory.inventorySurface.get_width()/2 - inventory.width /2,inventory.inventorySurface.get_height()/2 - inventory.height /2,inventory.width,inventory.height))
    
    innerScreenWidth = inventory.width - 50
    innerScreenHeight = inventory.height - 50
    pygame.draw.rect(inventory.inventorySurface,(0,0,1),(inventory.inventorySurface.get_width()/2 - innerScreenWidth/2, inventory.inventorySurface.get_height()/2 - innerScreenHeight/2, innerScreenWidth, innerScreenHeight))
    
    

    if inventory.width < inventory.finalWidth:
        inventory.width += (180 * pixelChange) * dt
        if inventory.width > inventory.finalWidth:
            inventory.width += inventory.finalWidth - inventory.width

    if inventory.height < inventory.finalHeight:
        inventory.height += (180 * pixelChange) * dt
        if inventory.height > inventory.finalHeight:
            inventory.height += inventory.finalHeight - inventory.height

    win.blit(inventory.inventorySurface,(win.get_width()/2 - inventory.inventorySurface.get_width() /2,win.get_height()/2 - inventory.inventorySurface.get_height() /2))




    if inventory.width >= inventory.finalWidth:
        TitleString = "Inventory Management Program"
        TitleFullString = "┌──────["
        TitleFullString += TitleString
        TileStringLen = 106-len(TitleFullString)
        
        for i in range(TileStringLen):
            if i == 0:
                TitleFullString += "]"
            elif i == TileStringLen-1:
                TitleFullString += "┐"
            elif i == 35-len(TitleString):
                TitleFullString += "┐"
            elif i == 36-len(TitleString):
                TitleFullString += "┌"
            else:
                TitleFullString += "─"
            
            
    

        ControlsString = "? = View Controls"
        ControlsFullString = "└──────["
        ControlsFullString += ControlsString
        ControlsStringLen = 106-len(ControlsFullString)
        for i in range(ControlsStringLen):
            if i == 0:
                ControlsFullString += "]"
            elif i == ControlsStringLen-1:
                ControlsFullString += "┘"
            elif i == 35-len(ControlsString):
                ControlsFullString += "┘"
            elif i == 36-len(ControlsString):
                ControlsFullString += "└"
            else:
                ControlsFullString += "─"

        
        Title = createText(win,ControlsFullString,"consolas",inventory.textColour,int(25*pixelChange))
        win.blit(Title,(220 * pixelChange,910 * pixelChange))

        Title = createText(win,TitleFullString,"consolas",inventory.textColour,int(25*pixelChange))
        win.blit(Title,(220 * pixelChange,130 * pixelChange))

        win.blit(inventory.exeTitle,(220 * pixelChange,170 * pixelChange))


        inventory.drawLineDown(win,pixelChange,1690)
        inventory.drawLineDown(win,pixelChange,822)
        inventory.drawLineDown(win,pixelChange,836)


        y = 210 * pixelChange

        if inventory.selectAnimationCount < inventory.selectAnimationMax/2:
            win.blit(inventory.selectIcon,(220 * pixelChange,y+ (inventory.selectVelocityX* inventory.selectX) ))
        
        inventory.selectAnimationCount += 1 *dt

        if inventory.selectAnimationCount > inventory.selectAnimationMax:
            inventory.selectAnimationCount = 0

        num = 1
        for eachItem in mainPlayer.inventory:
            win.blit(eachItem[2],(260 * pixelChange,y))
            y += inventory.selectVelocityX
            num += 1 
    
        inventory.drawItemInfo(win,mainPlayer,textureLayers,pixelChange)

        inventory.selectX
        if len(mainPlayer.inventory) > 0:
            row = 200  * pixelChange
            for eachRow in mainPlayer.inventory[inventory.selectX][3]:
                win.blit(eachRow,(1150 * pixelChange,row))
                row += 30 * pixelChange

    
    return inventory
