import pygame, sys
from changeFullscreen import *
from particleSystem import *
from menuFunctions import *
from updateTime import *
from setup import setupTime
from pygame.locals import *
from textCreator import *
from saving import *


def redrawCredits(creditsSurface,pixelChange,message):
    dedicatedText = createText(creditsSurface,message,"bahnschrift",(255,200,200),int(200 * pixelChange))
    creditsSurface.fill((168,63,57))
    creditsSurface.blit(dedicatedText,(creditsSurface.get_width()/2-dedicatedText.get_width()/2,creditsSurface.get_height()/2-dedicatedText.get_height()/2))
    backButton = textButton(creditsSurface,creditsSurface,pixelChange,"Back","bahnschrift",(255,255,255),30,int(30 * pixelChange),int(creditsSurface.get_height()-60 * pixelChange))


def credits(win,clock,pixelChange,fullscreen,framerate):
    creditsSurface = pygame.Surface((win.get_width(),win.get_height()), pygame. SRCALPHA)
    creditsSurface.fill((168,63,57))

    dedicatedText = createText(win,"Project Arctic","bahnschrift",(255,200,200),int(200 * pixelChange))
    creditsSurface.blit(dedicatedText,(creditsSurface.get_width()/2-dedicatedText.get_width()/2,creditsSurface.get_height()/2-dedicatedText.get_height()/2))
    backButton = textButton(win,creditsSurface,pixelChange,"Back","bahnschrift",(255,255,255),30,int(30 * pixelChange),int(win.get_height()-60 * pixelChange))

    rainGroup = rainParticleGroup(1,30)

    windX = 0
    clock, last_time = setupTime()

    timer = 0

    clickCounter = 0
    run = True
    while run:
        clock.tick(framerate)
        dt, last_time = updateTime(last_time)

        timer += 1 * dt
        if timer > 200 and timer <400:
            redrawCredits(creditsSurface,pixelChange,"Handcrafted by")
        elif timer > 400 and timer <600:
            redrawCredits(creditsSurface,pixelChange,"Kaya Arkin")
        elif timer > 600:
            redrawCredits(creditsSurface,pixelChange,"Thank you :)")

        for event in pygame.event.get():
            if event.type == QUIT: # Quites the game when pressing X
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN: # Quites the game when pressing ESC
                if event.key == K_ESCAPE:
                    run = False

                if event.key == K_f: # Toggles between fullscreen
                    fullscreen = not fullscreen
                    changeFullscreen(win,fullscreen)
        
        win.blit(creditsSurface,(0,0))

        mousePos, mousePress  = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        if mousePress[0] == True: # The button only activates when you click first time, not when holding button
            clickCounter += 1
        else:
            clickCounter = 0

        if backButton.backButtonCollision(mousePress,mousePos,clickCounter):
            run = False

        rainGroup.updateParicles(win,dt,windX,pixelChange)

        pygame.display.update()
    
## ------  New Game Menu  ------ ##
def newGameMenu(win,clock,pixelChange,fullscreen,framerate,randomWorld,mapWidth,mapHeight):
    newGameSurface = pygame.Surface((win.get_width(),win.get_height()), pygame. SRCALPHA)
    newGameSurface.fill((255,255,255))
    
    title = createText(win,"New Game","bahnschrift",(100,100,100),int(80 * pixelChange))
    newGameSurface.blit(title,((win.get_width()/2 - title.get_width() / 2)-(5* pixelChange),30* pixelChange))


    buttonSize = int(50 * pixelChange)
    firstButtonY = 200
    buttonYChange = 100
    buttonY = firstButtonY

    randomText = createText(win,"Randomise","bahnschrift",(100,100,100),buttonSize)
    newGameSurface.blit(randomText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    randomCheckbox = pygame.Rect(int(400 * pixelChange),int((buttonY+20) * pixelChange),int(30 * pixelChange),int(30 * pixelChange))
    buttonY += buttonYChange

    mapWidthText = createText(win,"Map Width","bahnschrift",(100,100,100),buttonSize)
    newGameSurface.blit(mapWidthText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    mapWidthSlider = slider(pixelChange,430,buttonY+20,300,40,30,30,mapWidth,200)
    buttonY += buttonYChange

    mapHeightText = createText(win,"Map Height","bahnschrift",(100,100,100),buttonSize)
    newGameSurface.blit(mapHeightText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    mapHeightSlider = slider(pixelChange,430,buttonY+20,300,40,30,30,mapHeight,200)
    buttonY += buttonYChange

    backButton = textButton(win,newGameSurface,pixelChange,"Back","bahnschrift",(100,100,100),30,int(30 * pixelChange),int(win.get_height()-60 * pixelChange))
    playButton = textButton(win,newGameSurface,pixelChange,"Play","bahnschrift",(100,100,100),30,int(win.get_width()-90 * pixelChange),int(win.get_height()-60 * pixelChange))

    clickCounter = 0
    newGame = False
    run = True
    while run:
        clock.tick(framerate)

        for event in pygame.event.get():
            if event.type == QUIT: # Quites the game when pressing X
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN: # Quites the game when pressing ESC
                if event.key == K_ESCAPE:
                    run = False

                if event.key == K_f: # Toggles between fullscreen
                    fullscreen = not fullscreen
                    changeFullscreen(win,fullscreen)


        mousePos, mousePress  = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        if mousePress[0] == True: # The button only activates when you click first time, not when holding button
            clickCounter += 1
        else:
            clickCounter = 0

        win.blit(newGameSurface,(0,0))

        randomWorld = checkBox(win,randomWorld,randomCheckbox,mousePress,mousePos,clickCounter,pixelChange)

        mapWidth = mapWidthSlider.updateSlider(win,mousePos,mousePress,pixelChange,mapWidth)
        mapWidthSlider.displayText(win,pixelChange,mapWidth,"bahnschrift",(100,100,100),30)

        mapHeight = mapHeightSlider.updateSlider(win,mousePos,mousePress,pixelChange,mapHeight)
        mapHeightSlider.displayText(win,pixelChange,mapHeight,"bahnschrift",(100,100,100),30)

        if backButton.backButtonCollision(mousePress,mousePos,clickCounter):
            run = False

        if playButton.backButtonCollision(mousePress,mousePos,clickCounter):
            run = False
            newGame = True


        pygame.display.flip()

    return randomWorld, mapWidth, mapHeight, newGame, fullscreen


## ------  Settings Menu  ------ ##
def settingsMenu(win,clock,pixelChange,fullscreen,framerate,FPS, alpha, weather, creative, chunkScaleNum, resolution):
    settingsSurface = pygame.Surface((win.get_width(),win.get_height()), pygame. SRCALPHA)

    settingsSurface.fill((255,255,255))
    title = createText(win,"Settings","bahnschrift",(100,100,100),int(80 * pixelChange))
    settingsSurface.blit(title,((win.get_width()/2 - title.get_width() / 2)-(5* pixelChange),30* pixelChange))

    buttonSize = int(50 * pixelChange)
    firstButtonY = 200
    buttonYChange = 100
    buttonY = firstButtonY

    resolutionText = createText(win,"Resolution","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(resolutionText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    resolutionSlider = slider(pixelChange,430,buttonY+20,300,40,30,30,resolution,8)
    buttonY += buttonYChange
    resolutionList = [
        "3840×2160", 
        "2560×1440", 
        "1920×1080", 
        "1600×900", 
        "1366×768",
        "1280×720"
    ]
    
    fullscreenCheckboxText = createText(win,"Fullscreen","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(fullscreenCheckboxText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    fullscreenCheckbox = pygame.Rect(int(400 * pixelChange),int((buttonY+20) * pixelChange),int(30 * pixelChange),int(30 * pixelChange))
    buttonY += buttonYChange

    framerateSliderText = createText(win,"Framerate","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(framerateSliderText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    framerateSlider = slider(pixelChange,430,buttonY+20,300,40,30,30,framerate,200)
    buttonY += buttonYChange

    FPSCheckboxText = createText(win,"Show FPS","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(FPSCheckboxText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    FPSCheckbox = pygame.Rect(int(400 * pixelChange),int((buttonY+20) * pixelChange),int(30 * pixelChange),int(30 * pixelChange))
    buttonY += buttonYChange

    alphaCheckboxText = createText(win,"Alpha","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(alphaCheckboxText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    alphaCheckbox = pygame.Rect(int(400 * pixelChange),int((buttonY+20) * pixelChange),int(30 * pixelChange),int(30 * pixelChange))
    buttonY += buttonYChange

    weatherCheckboxText = createText(win,"Weather","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(weatherCheckboxText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    weatherCheckbox = pygame.Rect(int(400 * pixelChange),int((buttonY+20) * pixelChange),int(30 * pixelChange),int(30 * pixelChange))
    buttonY += buttonYChange

    creativeCheckboxText = createText(win,"Creative","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(creativeCheckboxText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    creativeCheckbox = pygame.Rect(int(400 * pixelChange),int((buttonY+20) * pixelChange),int(30 * pixelChange),int(30 * pixelChange))
    buttonY += buttonYChange

    chunkScaleList = [
    "16", 
    "32", 
    "42", 
    "64",
    "80",
    "96"
    ]

    chunkSizeText = createText(win,"Chunk Size","bahnschrift",(100,100,100),buttonSize)
    settingsSurface.blit(chunkSizeText,(int(80 * pixelChange),int(buttonY * pixelChange)))
    chunkSizeSlider = slider(pixelChange,430,buttonY+20,300,40,30,30,chunkScaleNum,len(chunkScaleList))
    buttonY += buttonYChange

    backButton = textButton(win,settingsSurface,pixelChange,"Back","bahnschrift",(100,100,100),30,int(30 * pixelChange),int(win.get_height()-60 * pixelChange))
    applyResolutionButton = textButton(win,settingsSurface,pixelChange,"Apply Resolution","bahnschrift",(100,100,100),30,resolutionSlider.x+resolutionSlider.width+(250*pixelChange),resolutionSlider.y)
    
    changeResolutionBol = False
    clickCounter = 0
    run = True
    while run:
        clock.tick(framerate)

        for event in pygame.event.get():
            if event.type == QUIT: # Quites the game when pressing X
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN: # Quites the game when pressing ESC
                if event.key == K_ESCAPE:
                    run = False

                if event.key == K_f: # Toggles between fullscreen
                    fullscreen = not fullscreen
                    changeFullscreen(win,fullscreen)


        mousePos, mousePress  = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        if mousePress[0] == True: # The button only activates when you click first time, not when holding button
            clickCounter += 1
        
        else:
            clickCounter = 0

        win.blit(settingsSurface,(0,0))


        resolution = resolutionSlider.updateSlider(win,mousePos,mousePress,pixelChange,resolution)
        if resolution < 0:
            resolution = 0
        
        elif resolution > len(resolutionList)-1:
            resolution = len(resolutionList)-1
        resolutionSlider.displayText(win,pixelChange,resolutionList[resolution],"bahnschrift",(100,100,100),30)


        fullscreen = checkBoxFullscreen(win,fullscreen,fullscreenCheckbox,mousePress,mousePos,clickCounter,pixelChange)

        FPS = checkBox(win,FPS,FPSCheckbox,mousePress,mousePos,clickCounter,pixelChange)

        alpha = checkBox(win,alpha,alphaCheckbox,mousePress,mousePos,clickCounter,pixelChange)

        weather = checkBox(win,weather,weatherCheckbox,mousePress,mousePos,clickCounter,pixelChange)

        creative = checkBox(win,creative,creativeCheckbox,mousePress,mousePos,clickCounter,pixelChange)

        framerate = framerateSlider.updateSlider(win,mousePos,mousePress,pixelChange,framerate)
        
        if framerate < 10:
            framerate = 10

        framerateSlider.displayText(win,pixelChange,framerate,"bahnschrift",(100,100,100),30)

        chunkScaleNum = chunkSizeSlider.updateSlider(win,mousePos,mousePress,pixelChange,chunkScaleNum)
        if chunkScaleNum < 0:
            chunkScaleNum = 0
        elif chunkScaleNum > len(chunkScaleList)-1:
            chunkScaleNum = len(chunkScaleList)-1


        chunkSizeSlider.displayText(win,pixelChange,chunkScaleList[chunkScaleNum],"bahnschrift",(100,100,100),30)

        if backButton.backButtonCollision(mousePress,mousePos,clickCounter):
            run = False

        if applyResolutionButton.backButtonCollision(mousePress,mousePos,clickCounter):
            changeResolution(win,fullscreen,resolution,resolutionList)
            run = False
            changeResolutionBol = True



        

        pygame.display.flip()
    return fullscreen, framerate, FPS, alpha, weather, creative, chunkScaleNum, resolution, changeResolutionBol





## ------  Main Menu  ------ ##
def mainMenu(win,clock,newSave=False):
    pixelChange = pygame.display.Info().current_w / 1920

    menuSurface = pygame.Surface((win.get_width(),win.get_height()), pygame. SRCALPHA) # Creates a surface for the menu images and text to sit on

    title = pygame.image.load('data/images/text/title.png') # Loading the image into memory
    title = pygame.transform.scale(title,(int(title.get_width()*pixelChange),int(title.get_height()*pixelChange)))
    game = loadSave("data/saves/gameData.pkl")

    versionText = createText(win,"Version 2.21.0.1","bahnschrift",(100,100,100),int(30 * pixelChange))
    creditsText = createText(win,"Credits","bahnschrift",(100,100,100),int(30 * pixelChange))
    creditsButton = textButton(win,menuSurface,pixelChange,"Apply Resolution","bahnschrift",(100,100,100),30,win.get_width()-creditsText.get_width()-30* pixelChange,win.get_height()-60 * pixelChange)


    menuSurface.fill((255,255,255))

    menuSurface.blit(title,((win.get_width()/2 - title.get_width() / 2)+(10* pixelChange),(win.get_height()/2 - title.get_height() / 2)-(250* pixelChange)))

    menuSurface.blit(versionText,(30* pixelChange,int(win.get_height()-60 * pixelChange)))

    menuSurface.blit(creditsText,(win.get_width()-creditsText.get_width()-30* pixelChange,int(win.get_height()-60 * pixelChange)))


    buttonSize = int(50 * pixelChange)
    firstButtonY = 510
    buttonYChange = 100
    
    buttonY = firstButtonY
    continueButtonText = createText(win,"Continue","bahnschrift",(100,100,100),buttonSize)
    rectContinueCollision = pygame.Rect(win.get_width()/2 - continueButtonText.get_width() / 2, buttonY* pixelChange,continueButtonText.get_width(),continueButtonText.get_height())
    buttonY += buttonYChange

    newSaveButtonText = createText(win,"New Save","bahnschrift",(100,100,100),buttonSize)
    rectnewSaveCollision = pygame.Rect(win.get_width()/2 - newSaveButtonText.get_width() / 2, buttonY* pixelChange,newSaveButtonText.get_width(),newSaveButtonText.get_height())
    buttonY += buttonYChange

    settingsButtonText = createText(win,"Settings","bahnschrift",(100,100,100),buttonSize)
    rectSettingsCollision = pygame.Rect(win.get_width()/2 - settingsButtonText.get_width() / 2, buttonY* pixelChange,settingsButtonText.get_width(),settingsButtonText.get_height())
    buttonY += buttonYChange

    exitButtonText = createText(win,"Exit","bahnschrift",(100,100,100),buttonSize)
    rectExitCollision = pygame.Rect(win.get_width()/2 - exitButtonText.get_width() / 2, buttonY* pixelChange,exitButtonText.get_width(),exitButtonText.get_height())
    buttonY += buttonYChange

    buttonRectList = [[continueButtonText,rectContinueCollision,"Continue"],[newSaveButtonText,rectnewSaveCollision,"New Save"],[settingsButtonText,rectSettingsCollision,"Settings"],[exitButtonText,rectExitCollision,"Exit"]]

    fullscreen = game.fullscreen
    changeFullscreen(win,fullscreen)
    FPS = game.FPS
    framerate = game.framerate
    alpha = game.alpha
    weather = False
    randomWorld = True
    mapWidth = 50
    mapHeight = 50
    creative = False
    chunkScaleNum = 3
    resolution = game.resolution

    changeResolutionBol = False

    clickCounter = 0
    run = True
    while run:
        clock.tick(framerate)

        for event in pygame.event.get():
            if event.type == QUIT: # Quites the game when pressing X
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN: # Quites the game when pressing ESC
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_f: # Toggles between fullscreen
                    fullscreen = not fullscreen
                    changeFullscreen(win,fullscreen)

        mousePos, mousePress  = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        if mousePress[0] == True: # The button only activates when you click first time, not when holding button
            clickCounter += 1
        else:
            clickCounter = 0

        for eachButton in buttonRectList:
            
            if eachButton[1].collidepoint(mousePos):
                eachButton[0] = createText(win,eachButton[2],"bahnschrift",(255, 192, 0),buttonSize)

                if mousePress[0] == True and clickCounter == 1:
                    if eachButton[2] == "Continue":
                        newSave = False
                        run = False

                    elif eachButton[2] == "Settings":
                        fullscreen, framerate, FPS, alpha, weather,creative, chunkScaleNum, resolution, changeResolutionBol = settingsMenu(win,clock,pixelChange,fullscreen,framerate,FPS,alpha,weather,creative, chunkScaleNum,resolution)

                    elif  eachButton[2] == "New Save":
                        randomWorld, mapWidth, mapHeight, newSave, fullscreen = newGameMenu(win,clock,pixelChange, fullscreen,framerate,randomWorld,mapWidth,mapHeight)
                        if newSave == True:
                            run = False


                    elif  eachButton[2] == "Exit":
                        pygame.quit()
                        sys.exit()

            else:
                eachButton[0] = createText(win,eachButton[2],"bahnschrift",(100,100,100),buttonSize)

        win.blit(menuSurface,(0,0))

        buttonY = firstButtonY
        for eachButton in buttonRectList:
            win.blit(eachButton[0],(win.get_width()/2 - eachButton[0].get_width() / 2, buttonY* pixelChange))
            buttonY += buttonYChange
        
        if creditsButton.backButtonCollision(mousePress,mousePos,clickCounter):
            credits(win,clock,pixelChange, fullscreen,framerate)
       
        pygame.display.flip()

        if changeResolutionBol == True:
            run = False
            changeResolutionBol = False
            game.resolution = resolution
            game.fullscreen = fullscreen
            game.framerate = framerate
            game.alpha = alpha
            game.FPS = FPS
            saveGame("data/saves/gameData.pkl",game)
            newSave, framerate, FPS, alpha, weather, randomWorld, mapWidth, mapHeight, creative, chunkScaleNum = mainMenu(win,clock,newSave)


    return newSave, framerate, FPS, alpha, weather, randomWorld, mapWidth, mapHeight, creative, chunkScaleNum