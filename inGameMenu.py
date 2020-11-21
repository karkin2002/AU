import pygame
from textCreator import *
from menuFunctions import *
from printTerminal import printTerminal

## Creates a dictionary with each texture to be placed on the menu with each x/y location and 
def loadingMenuItems(win,chunkSize,pixelChange,num,pageNum,distanceBetween,menuRectCollisionDic,x,y,menuLayers,layerDic):
    for i in layerDic:
        menuRectCollisionDic[i] = pygame.Rect(x,y,chunkSize,chunkSize)
        menuLayers[num] = [i,menuRectCollisionDic[i]]

        if x + distanceBetween < win.get_width()-80*pixelChange:
            x += distanceBetween

        else:
            x = win.get_width()/2+60* pixelChange
            y += distanceBetween

        num += 1

        if num % pageNum == 0:
            x = win.get_width()/2+60* pixelChange
            y = 100 * pixelChange
            
    return layerDic, pageNum, num, x, y


## Sets up the in game building menu
def inGameMenuSetUp(win,alpha,pixelChange,chunkSize,textureLayers):

    if alpha == True:
        ## Creates a surface for the menu with an alpha of 150
        menuSurface = pygame.Surface((win.get_width()/2-60*pixelChange,win.get_height()-60*pixelChange))
        menuSurface.set_colorkey((0,0,0))
        menuSurface.set_alpha(150)
        pygame.draw.rect(menuSurface,(200,200,200),(0,0,menuSurface.get_width(),menuSurface.get_height()))
    else:
        menuSurface = pygame.Surface((win.get_width()/2-60*pixelChange,win.get_height()-60*pixelChange))
        menuSurface.fill((200,200,200))


    menuRectCollisionDic = {} # Stores rect for each menu item
    menuTextList = [] # Stores text for each menu item

    menuLayers = {}

    ## Goes through each item of the texture dic and
    ## static object dic adds it's rect to menuRectCollisionDic
    ## with its x and y coordinate
    x = win.get_width()/2+60* pixelChange
    y = 100 * pixelChange
    distanceBetween = 20* pixelChange + chunkSize
    pageNum = 81
    num = 0

    ## Initialising the items in them menu
    textureLayers.groundLayerDic, pageNum, num, x, y = loadingMenuItems(win,chunkSize,pixelChange,num,pageNum,distanceBetween,menuRectCollisionDic,x,y,menuLayers,textureLayers.groundLayerDic)

    textureLayers.surfaceLayerDic, pageNum, num, x, y = loadingMenuItems(win,chunkSize,pixelChange,num,pageNum,distanceBetween,menuRectCollisionDic,x,y,menuLayers,textureLayers.surfaceLayerDic)

    textureLayers.objectLayerDic, pageNum, num, x, y = loadingMenuItems(win,chunkSize,pixelChange,num,pageNum,distanceBetween,menuRectCollisionDic,x,y,menuLayers,textureLayers.objectLayerDic)


    menuTitle = createText(win,"Select a chunk:","bahnschrift",(0,0,0),int(30 * pixelChange)) # Menu Title Text


    menuTextList.append([menuTitle,win.get_width()/2+60*pixelChange,45*pixelChange]) # List used to display all the text needed on the menu

    ## Initialising back and foward buttons for the main menu
    backButton = colourButton(pixelChange,1000,1000,40,40,(200,100,100),3)

    frontButton = colourButton(pixelChange,1840,1000,40,40,(200,100,100),3)

    printTerminal("Info",f"Loaded '{len(menuLayers)}' textures") # Printing to terminal how many textures have been loaded

    return menuSurface, menuRectCollisionDic, menuTextList, backButton, frontButton,menuLayers, pageNum


def ingameMenu(win,textureLayers,chunkSize,menuSurface,alpha,menuRectCollisionDic,mousePos,mousePress,place,pixelChange,menuTextList,backButton,frontButton,clickCounter,menuLayers,pageNum):

    ## Displayes either the alpha menu background or a solid one
    win.blit(menuSurface,(win.get_width()/2+30*pixelChange,30*pixelChange))
    
    ## Goes through each item in both texture dic and
    ## static object dic and blits it onto a surface as
    ## well as checking collisions
    x = win.get_width()/2+60* pixelChange
    y = 100 * pixelChange
    distanceBetween = 20* pixelChange + chunkSize
    

    for eachNum in menuLayers:
        if eachNum < pageNum and eachNum >= pageNum-81:
        
            try:
                win.blit(textureLayers.groundLayerDic[menuLayers[eachNum][0]],(x,y))
            except:
                
                try:
                    win.blit(textureLayers.surfaceLayerDic[menuLayers[eachNum][0]],(x,y))
                except: 
                    
                    try:
                        win.blit(textureLayers.objectLayerDic[menuLayers[eachNum][0]],(x,y))
                    except:
                        printTerminal("ERROR",f"Texture '{menuLayers[eachNum][0]}' not loaded'")

            if menuLayers[eachNum][1].collidepoint(mousePos) and mousePress[0] == True:
                place = menuLayers[eachNum][0]
            
            
            if x + distanceBetween < win.get_width()-80*pixelChange:
                x += distanceBetween
            
            else:
                x = win.get_width()/2+60* pixelChange
                y += distanceBetween
    
    
    ## Displays text used on the menu
    for i in menuTextList:
        win.blit(i[0],(i[1],i[2]))

    backButton.displayButton(win,pixelChange)
    frontButton.displayButton(win,pixelChange)
    
    if backButton.collision(mousePos,mousePress,clickCounter):
        if pageNum != 81:
            pageNum -= 81

    
    elif frontButton.collision(mousePos,mousePress,clickCounter):
        if pageNum < len(menuLayers):
            pageNum += 81
    
    return place,pageNum