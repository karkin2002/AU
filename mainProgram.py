import pygame, random, sys, time, concurrent.futures, pickle, datetime
from changeFullscreen import changeFullscreen
from particleSystem import *
from pygame.locals import *
from textCreator import createText
from player import player, staticEntity
from camera import camera
from inGameMenu import loadingMenuItems, inGameMenuSetUp, ingameMenu
from chunkClass import chunk
from updateTime import updateTime
from FPSMonitor import SetupFPS, updateFPS, updateFPSDisplay
from displayMap import backgroundSurfaceSetup, backgroundSurfaceUpdate,spaceBackdrop
from renderMap import renderMap
from gameData import gameData
from mainMenu import *
from readingTextfiles import openItems, openMapArray
from setup import *
from displayInventory import openInventory, inventoryWindow
from checkPoint import loadMapCheckPoint, booleanCheckPoint, teleportCheckPoint
from cutscene import fade
import config
config.init()
pygame.init()

print ("""

       ---- Map Creator ----
-----------------------------------

- Made by Kaya Arkin

-----------------------------------


-----------------------------------
Controls:
    - Movement = wasd
    - Arrow Keys = rain angle / camera speed
    - Select / Place Item = LMC
    - Menu = TAB
    - Delete Object = E
    - Save World = J
    - Fullscreen = F
    - 1 = delete groundLayer
    - 2 = delete surfaceLayer
    - 3 = delete objectLayer
    - 4 = place smoke effect
    - ESC = back / close

-----------------------------------
""")
printTerminal("Info","Starting 'mainProgram()'")


## Player selects from tkinter menu: winWidth, winHeight,
## fullscreen, framerate, newSave, mapWith, mapHeight
def mainProgram(mapName, newStart = True, win = None, newSave = None, framerate = None, FPS = None, alpha = None, weather = None, randomWorld = None, creative = None, chunkScaleNum = None, mapWidth = None, mapHeight = None):


    game = loadSave("data/saves/gameData.pkl")
    resolutionList = [
        "3840×2160", 
        "2560×1440", 
        "1920×1080", 
        "1600×900", 
        "1366×768",
        "1280×720",
    ]

    fullscreen = game.fullscreen
    resolution = game.resolution
    resolution = resolutionList[resolution]
    resolution = resolution.split("×")
    winWidth = int(resolution[0])
    winHeight = int(resolution[1])
    resolutionDefult = game.resolution

    if newStart == True:
        win, monitor_size = setupDisplay(winWidth, winHeight, fullscreen) # Setup Window
        clock = pygame.time.Clock() # Setup Clock

        newSave, framerate, FPS, alpha, weather, randomWorld, mapWidth, mapHeight, creative, chunkScaleNum = mainMenu(win,clock)

        ## Threading used to setup game and display loading screen
        executor = concurrent.futures.ThreadPoolExecutor() # Starting setup thread
        threadStartup = executor.submit(setup,[win,newSave,resolutionDefult,fullscreen,framerate,mapWidth,mapHeight,alpha,FPS,randomWorld,chunkScaleNum,mapName])

        if newSave == False:
            groundMapArray, gridRef = openMapArray(mapName)


        ## ------  Loading Screen  ------ ##
        pixelChange = pygame.display.Info().current_w / 1920 # Compansating for window size
        loadngText = createText(win,"---","bahnschrift",(0,0,0),int(28 * pixelChange))
        stageArray = ["Starting new thread", "Setting up time", "Loading player and NPC data", "Setting up sizes", "Loading textures", "Creating new ground array: 0%", "Saving", "Loading Save", "Creating Ground Texture Surface: 0%"]
        loadingTextList = ["Loading", "Loading.", "Loading..", "Loading..."]

        for i in range(len(loadingTextList)):
            loadingTextList[i] = createText(win,loadingTextList[i],"bahnschrift",(0,0,0),int(90 * pixelChange)) # Initialising loading text using the loadingTextList List

        config.stage = 0
        config.loadingNum = 0
        config.loadingRun = True

        ## Stages linked to startup.py
        num = 0 
        i = 0
        while config.stage < 9:
            clock.tick(framerate)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            win.fill((255,255,255))
            
            win.blit(loadingTextList[i],((win.get_width()//2)-loadingTextList[0].get_width()//2,(win.get_height()//2)-loadingTextList[0].get_height()//2)) # Display loading... text
        
            if config.stage == 5:
                if randomWorld == True:
                    stageArray[5] = f"Creating new randomised ground array: {int(config.loadingNum/mapHeight*100)}%" # Percentage of map complete
                
                else:
                    stageArray[5] = f"Creating new plain ground array: {int(config.loadingNum/mapHeight*100)}%" # Percentage of map complete
            
            elif config.stage == 8:
                if newSave == True:
                    stageArray[8] = f"Creating Ground Texture Surface: {int(config.loadingNum/mapHeight*100)}%" # Percentage of map complete
                else:
                    stageArray[8] = f"Creating Ground Texture Surface: {int(config.loadingNum/len(groundMapArray)*100)}%" # Percentage of map complete

            if config.stage < 9:
                loadngText = createText(win,stageArray[config.stage],"bahnschrift",(0,0,0),int(28 * pixelChange))
            
            
            win.blit(loadngText,(int(win.get_width()/2 - loadngText.get_width() / 2),int((win.get_height()/2 - loadngText.get_height() / 2)+(80* pixelChange)))) # Display Loading information

            pygame.display.flip()

            if num >= framerate:
                num = 0 
                if i < 3 :
                    i += 1
                else:
                    i = 0
            num += 5
        clock, last_time, mapWidth, mapHeight, chunkSize, pixelChange, textureLayers, game, backgroundSurface, groundMapArray, gridRef = threadStartup.result() # Results from the thread

        fade1 = fade(win,(255,0,0),False)
    
    else:
        if mapName == "Level1" or mapName == "Level2" or mapName == "Level3" or mapName == "Level4":
            chunkScaleNum = 5
            fade1 = fade(win,(255,0,0),True)

        else:
            fade1 = fade(win,(255,0,0),False)

        clock, last_time, mapWidth, mapHeight, chunkSize, pixelChange, textureLayers, game, backgroundSurface, groundMapArray, gridRef = setup([win,newSave,resolutionDefult,fullscreen,framerate,mapWidth,mapHeight,alpha,FPS,randomWorld,chunkScaleNum,mapName])










    ## Used to display FPS
    sec, frames, nextFPStime, framesText = SetupFPS()
    
    items = openItems()



    ## ------  Main Program  ------ ##
    playerChunkDifference = chunkSize/16
    mapX = win.get_width() / 2
    mapY = win.get_height() / 2
    if mapName == "Level1" or mapName == "Level2" or mapName == "Level3" or mapName == "Level4":
        mainPlayer = player(chunkSize,pixelChange,mapX,mapY,int(15.83*playerChunkDifference),int(24.16*playerChunkDifference),"data/images/textures/underPlayer/")
        game.velocity = 6
    else:
        mainPlayer = player(chunkSize,pixelChange,mapX,mapY,int(16*playerChunkDifference),int(21*playerChunkDifference),"data/images/textures/player/")
        game.velocity = 4.6
        dulpertaleTitle = pygame.image.load("data/images/text/dulpertale.png")
    
    mainCamera = camera(pixelChange,win,360,360) # Times the variables by the pixelChange for you


    if mapName == "Level2":
        flower = staticEntity(win,pixelChange,playerChunkDifference,70,210,int(21*playerChunkDifference),int(21*playerChunkDifference),"data/images/textures/entity/flower/",16,8)
        freezeCheckPoint = booleanCheckPoint(0,242,150,2,pixelChange,playerChunkDifference,"Level2")
    else:
        freezeCheckPoint = booleanCheckPoint(0,0,0,0,pixelChange,playerChunkDifference,"Level2")
        if mapName == "Level4":
            flower = staticEntity(win,pixelChange,playerChunkDifference,2000,105,int(21*playerChunkDifference),int(22*playerChunkDifference),"data/images/textures/entity/flowerDance/",72,8)
    
    if mapName == "Level3":
        room1 = teleportCheckPoint(798,382,21,2,pixelChange,playerChunkDifference,[77,10])
        room1Back = teleportCheckPoint(1215,175,33,2,pixelChange,playerChunkDifference,[50, 24])

    ## Setup Audio
    if weather == True:
        pygame.mixer.music.load("data/sound/rainSound.wav")
        pygame.mixer.music.play(-1)

    inventoryOpenSound = pygame.mixer.Sound("data/sound/inventoryOpenSound.wav")

    dulpertaleInto = pygame.mixer.Sound("data/sound/dulpertaleIntro.wav")
    dulpertaleIntoSound = False


    ## Check Points
    checkPointList = [loadMapCheckPoint(1914,860,28,22,pixelChange,playerChunkDifference,"Map1","Level1"),loadMapCheckPoint(465,90,60,2,pixelChange,playerChunkDifference,"Level1","Level2"),loadMapCheckPoint(51,110,60,2,pixelChange,playerChunkDifference,"Level2","Level3"),loadMapCheckPoint(570,345,2,20,pixelChange,playerChunkDifference,"Level3","Level4")]


    ## Setup Rain Particles and wind
    rainGroup = rainParticleGroup(22,90)
    windX = 2

    menuSurface, menuRectCollisionDic, menuTextList, backButton, frontButton,menuLayers,pageNum = inGameMenuSetUp(win,alpha,pixelChange,chunkSize,textureLayers)

    clickCounter = 0

    place = "deleteObject"

    game.gridRef = gridRef

    inventory = inventoryWindow(win,pixelChange,alpha)

    if creative == False:
        mapX -= game.gridRef[0]*chunkSize
        mapY -= (game.gridRef[1]-1)*chunkSize
        mainPlayer.x = mapX + game.gridRef[0]*chunkSize
        mainPlayer.y = mapY + (game.gridRef[1]-1)*chunkSize

    try:
        timer = 0
        dulpertaleTitleY = -dulpertaleTitle.get_height() - 100*pixelChange
        dulpertaleTitleVelocity = 2 * pixelChange
    except:
        pass

    mainPlayer.direction = None

    if mapName == "Level2" or mapName == "Level3":
        mainPlayer.lastPosition = mainPlayer.animationList[3][0]
    elif mapName == "Level4":
        mainPlayer.lastPosition = mainPlayer.animationList[2][0]
        spaceSurface1, spaceSurfaceX1, spaceSurfaceY1 = spaceBackdrop(win,pixelChange,400)

    ## -------  Main Loop  ------ ##
    run = True
    while run:

        ## Framerate and delta time
        clock.tick(framerate)
        dt, last_time = updateTime(last_time)


        for event in pygame.event.get():
            if event.type == QUIT: # Quites the game when pressing X
                pygame.quit()
                sys.exit()         
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    newStart = True

                if event.key == K_f: # Toggles between fullscreen
                    fullscreen = not fullscreen # Toggles function
                    changeFullscreen(win,fullscreen)
                
                elif event.key == K_j: # Saves the game Data
                    saving = createText(win,f"Saving {game} to data/saves/gameSave.pkl","bahnschrift",(255,255,255),int(20*pixelChange))
                    win.blit(saving,((win.get_width() - saving.get_width())-10,(win.get_height() - saving.get_height())-10))
                    pygame.display.flip()
                    if creative == False:
                        game.gridRef = mainPlayer.gridRef
                    saveGame('data/saves/gameData.pkl',game)
                    saveMap(mapName,groundMapArray,game.gridRef)
                
                elif event.key == K_r:
                    weather = not weather
                
                if creative == True and fade1.fading == False:
                    if event.key == K_1:
                        place = "deleteGround"

                    elif event.key == K_2:
                        place = "deleteSurface"

                    elif event.key == K_3:
                        place = "deleteObject"
                    
                    elif event.key == K_4:
                        place = "particle"
                    
                    elif event.key == K_c:
                        place = "collision"
                    
                    elif event.key == K_x:
                        place = "deleteCollision"
                
                else:
                    if groundMapArray[mainPlayer.gridRef[1]][mainPlayer.gridRef[0]].objectLayer != None:
                        if event.key == K_e:
                            for i in items:
                                if groundMapArray[mainPlayer.gridRef[1]][mainPlayer.gridRef[0]].objectLayer == i[1]:
                                    
                                    ## Checks to see if that item is already in the inventory
                                    ## it it is instead of adding another item into the list
                                    ## it adds one to the amount of that item in the list
                                    present = False
                                    for eachItem in mainPlayer.inventory:
                                        if eachItem[0] == i and eachItem[1] < 64:
                                            eachItem[1] += 1
                                            eachItem[2] = createText(win,f"[{mainPlayer.inventory.index(eachItem)}]- {i[0]} x{eachItem[1]}","consolas",inventory.textColour,int(25*pixelChange))
                                            present = True
                                            break
                                    
                                    ## Adds a new item if it can't already be found in the inventory
                                    if present == False:
                                        descriptionList = []
                                        for num in range(len(i[2])):
                                            if num == 36:
                                                descriptionList.append(createText(win,i[2][:num],"consolas",inventory.textColour,int(25*pixelChange)))
                                            elif num % 36 == 0:
                                                descriptionList.append(createText(win,i[2][num-36:num],"consolas",inventory.textColour,int(25*pixelChange)))
                                        
                                        descriptionList.append(createText(win,i[2][num-(num%36):],"consolas",inventory.textColour,int(25*pixelChange)))
                                        if int(i[5]) <= mainPlayer.intelligence:
                                            mainPlayer.inventory.append([i,1,createText(win,f"[{str(len(mainPlayer.inventory))}]- {i[0]} x{1}","consolas",inventory.textColour,int(25*pixelChange)),descriptionList])
                                        else:
                                            mainPlayer.inventory.append([i,1,createText(win,f"[{str(len(mainPlayer.inventory))}]- {i[3]} x{1}","consolas",inventory.textColour,int(25*pixelChange)),descriptionList])
                                    
                                    groundMapArray[mainPlayer.gridRef[1]][mainPlayer.gridRef[0]].objectLayer = None
                                    backgroundSurfaceUpdate(backgroundSurface,groundMapArray[mainPlayer.gridRef[1]][mainPlayer.gridRef[0]],groundMapArray[mainPlayer.gridRef[1]],groundMapArray,chunkSize,textureLayers)
                    
                    if freezeCheckPoint.trigger == True:
                        flower.textBoxMessageNum += 1
                    
                if creative == False:

                    
                    if event.key == K_w:
                        if inventory.selectX > 0:
                                inventory.selectX -= 1
                    
                    elif event.key == K_s:
                        if inventory.selectX < len(mainPlayer.inventory)-1:
                            inventory.selectX += 1


        ## Fading Screen
        if mapName == "Level1":
            fade1.fadeOut(0.5,dt)
        elif mapName != "Map1":
            fade1.fadeOut(5,dt)
        
                

        keys = pygame.key.get_pressed()

        ## Hold to open ingame menu
        if keys[pygame.K_TAB]:
            if pygame.mixer.get_busy() == 0 and game.inGame == True and creative == False and fade1.fading == False:
                pygame.mixer.Sound.play(inventoryOpenSound)
            game.inGame = False
        else:
            game.inGame = True
            inventory = inventoryWindow(win,pixelChange,alpha)

        mainPlayer.move(dt)
        mousePos, mousePress  = pygame.mouse.get_pos(), pygame.mouse.get_pressed() # Mouses position and press
        
        if mousePress[0] == True: # The button only activates when you click first time, not when holding button
            clickCounter += 1
        else:
            clickCounter = 0

        if mapName == "Map1":
            win.fill((58, 190, 65)) # Filling background
        else:
            win.fill((0,0,0)) # Filling background
            if mapName == "Level4":
                win.blit(spaceSurface1,(spaceSurfaceX1,spaceSurfaceY1))


        ## Display background
        backgroundSurface, groundMapArray = renderMap(win,groundMapArray,chunkSize,textureLayers,pixelChange,mapX,mapY,mousePos,mousePress,place,game.inGame,creative,backgroundSurface,mapHeight,mapWidth,dt,clickCounter) # Draws the map

        ## Displaying Player and Collisions
        if creative == False:
            if mapName == "Level2":
                flower.move(dt)
                flower.draw(win,mapX,mapY)
                if freezeCheckPoint.trigger == True:
                    flower.displayText(win,dt)
                    flower.direction = "talking"
                else:
                    flower.direction = "None"
            elif mapName == "Level4":
                flower.move(dt)
                flower.draw(win,mapX,mapY)
                flower.direction = "talking"

            ## Display Collisions
            mainPlayer.drawPlayer(win)
            # mainPlayer.drawCollision(win,mapX,mapY,chunkSize)
            # mainCamera.drawCollision(win)

        ## Update/Display Rain Particles
        if weather == True:
            rainGroup.updateParicles(win,dt,windX,pixelChange)
        
        if mapName == "Level3":
            mapX, mapY, mainPlayer = room1.teleportPlayer(win,mainPlayer,mapX,mapY,chunkSize)
            room1.update(mapX,mapY)
            # room1.draw(win)

            mapX, mapY, mainPlayer = room1Back.teleportPlayer(win,mainPlayer,mapX,mapY,chunkSize)
            room1Back.update(mapX,mapY)
            # room1Back.draw(win)

        ## Placing Blocks Menu
        if game.inGame == False:
            if creative == True:
                place,pageNum = ingameMenu(win,textureLayers,chunkSize,menuSurface,alpha,menuRectCollisionDic,mousePos,mousePress,place,pixelChange,menuTextList, backButton, frontButton,clickCounter,menuLayers,pageNum)
            else:
                inventory = openInventory(win,dt,inventory, mainPlayer,pixelChange,textureLayers)

        else:
            if freezeCheckPoint.trigger == False:
                velocityAmount = game.velocity * dt
                if creative == False:
                    if fade1.fading == False:
                        if keys[pygame.K_w]:
                            if not mainPlayer.checkCollisions(win,0,-(velocityAmount+1)):
                                if mainCamera.collisionRect.contains(pygame.Rect(mainPlayer.x,mainPlayer.y - velocityAmount,mainPlayer.width,mainPlayer.height)):
                                    mainPlayer.y -= velocityAmount
                                else:
                                    mapY += velocityAmount
                                    if mapName == "Level4":
                                        spaceSurfaceY1 += (game.velocity/20)* dt
                                mainPlayer.direction = "up"

                        
                        elif keys[pygame.K_s]:
                            if not mainPlayer.checkCollisions(win,0,(velocityAmount+1)):
                                if mainCamera.collisionRect.contains(pygame.Rect(mainPlayer.x,mainPlayer.y + velocityAmount,mainPlayer.width,mainPlayer.height)):
                                    mainPlayer.y += velocityAmount
                                else:
                                    mapY -= velocityAmount
                                    if mapName == "Level4":
                                        spaceSurfaceY1 -= (game.velocity/20)* dt
                                mainPlayer.direction = "down"


                        if keys[pygame.K_d]:
                            if not mainPlayer.checkCollisions(win,(velocityAmount+1),0):
                                if mainCamera.collisionRect.contains(pygame.Rect(mainPlayer.x + velocityAmount,mainPlayer.y,mainPlayer.width,mainPlayer.height)):
                                    mainPlayer.x += velocityAmount
                                else:
                                    mapX -= velocityAmount
                                    if mapName == "Level4":
                                        spaceSurfaceX1 -= (game.velocity/20)* dt
                                mainPlayer.direction = "right"


                        elif keys[pygame.K_a]:
                            if not mainPlayer.checkCollisions(win,-(velocityAmount+1),0):
                                if mainCamera.collisionRect.contains(pygame.Rect(mainPlayer.x - velocityAmount,mainPlayer.y,mainPlayer.width,mainPlayer.height)):
                                    mainPlayer.x -= velocityAmount
                                else:
                                    mapX += velocityAmount
                                    if mapName == "Level4":
                                        spaceSurfaceX1 += (game.velocity/20)* dt
                                mainPlayer.direction = "left"




                        elif not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
                            mainPlayer.direction = None
                        
                        mainPlayer.updateGridRef(win,chunkSize,mapX,mapY,groundMapArray)
                else:
                    if keys[pygame.K_w]:
                        mapY += velocityAmount

                    if keys[pygame.K_s]:
                        mapY -= velocityAmount

                    if keys[pygame.K_d]:
                        mapX -= velocityAmount
                    
                    if keys[pygame.K_a]:
                        mapX += velocityAmount
                
                if keys[pygame.K_UP]:
                        game.velocity += 0.1
                    
                elif keys[pygame.K_DOWN]:
                    if game.velocity >= 0:
                        game.velocity -= 0.1

                ## Change wind direction
                if weather == True:
                    if keys[pygame.K_RIGHT]:
                        windX += 1 * dt
                    
                    if keys[pygame.K_LEFT]:
                        windX -= 1 * dt
            
            else:
                mainPlayer.direction = "None"
    
        fade1.draw(win)

        ## Updating FPS counter
        if FPS == True:
            frames, nextFPStime, framesText = updateFPSDisplay(sec, frames, nextFPStime, win,pixelChange,framesText)
        
        if creative == False:

            if mapName == "Level2":
                freezeCheckPoint.update(mapX,mapY)
                # freezeCheckPoint.draw(win)
                freezeCheckPoint.checkCollision(mainPlayer.playerCollisionRect)
                


            ## Iterates through check point list checking whether the player had a collision with it
            for eachCheckpoint in checkPointList:
                if mapName == eachCheckpoint.mapNameFrom:
                    eachCheckpoint.update(mapX,mapY)
                    
                    ## Next Map name set to the check points mapNameTo
                    if eachCheckpoint.checkCollision(mainPlayer.playerCollisionRect):
                        if mapName == "Map1":

                            if fade1.fading == False:
                                if dulpertaleTitleY < win.get_height()/2-dulpertaleTitle.get_height():
                                    dulpertaleTitleY += dulpertaleTitleVelocity*dt
                                else:
                                    if dulpertaleIntoSound == False:
                                        pygame.mixer.Sound.play(dulpertaleInto)
                                    dulpertaleIntoSound = True
                                    timer += 1 * dt


                            if timer >= 400:
                                if fade1.fading == False:
                                    newStart = eachCheckpoint.mapNameTo
                                    run = False
                            else:
                                fade1.fadeIn(2,dt)
                                if fade1.fading == False:
                                    win.blit(dulpertaleTitle,(win.get_width()/2-dulpertaleTitle.get_width()/2,dulpertaleTitleY))
                        else:
                            newStart = eachCheckpoint.mapNameTo
                            run = False
                
                    # eachCheckpoint.draw(win)
        
        if mapName == "Level2":
            if flower.textBoxMessageNum == 12:
                freezeCheckPoint.collisionRect = pygame.Rect(0,0,1,1)
                freezeCheckPoint.trigger = False

        pygame.display.flip()

    return newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight



while True:

    pygame.mouse.set_visible(True)
    newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight = mainProgram("Map1",True)
    printTerminal("Info","Restarting 'mainProgram()'")


    if newStart != True:
        pygame.mixer.music.stop()
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load("data/sound/FallenDown.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.06)
        newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight = mainProgram(newStart,newStart, win, newSave, framerate, FPS, alpha, False, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight)


    if newStart != True:
        pygame.mixer.music.load("data/sound/friend.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.06)
        newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaaleNum, mapWidth, mapHeight = mainProgram(newStart,newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight)
    
    
    if newStart != True:
        pygame.mixer.music.load("data/sound/home.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.08)
        newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight = mainProgram(newStart,newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight)
    
    if newStart != True:
        pygame.mixer.music.load("data/sound/HomeMusicBox.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.08)
        newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight = mainProgram(newStart,newStart, win, newSave, framerate, FPS, alpha, weather, randomWorld, creative, chunkScaleNum, mapWidth, mapHeight)

    pygame.mixer.music.stop()