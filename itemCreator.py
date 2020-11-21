import pygame, random, sys, time, concurrent.futures, pickle, datetime, ctypes
from pygame.locals import *
from textCreator import *
from menuFunctions import *
from tkinter import *
from tkinter.filedialog import askopenfilename
pygame.init()


## Close tkinter window
def closeSaveRoot(root,filenameEntry,save):
    global filename
    if save == False:
        filenameEntry.delete(0, END)
        filenameEntry.insert(0, "")
    filename = filenameEntry.get()
    root.destroy()

## Tkinter Save Program
def saveOptions():
    root = Tk()
    root.title("Save Texture")
    root.resizable(width=False, height=False)

    Title = Label(root, text="Save Texture").grid(row=0,column=0,columnspan=2)
    
    filenameText = Message(root,text="Filename:",width = 100).grid(row=1,column=0)
    filenameEntry = Entry(root,width = 20)
    filenameEntry.insert(0, "TextureName")
    filenameEntry.grid(row=1,column=1)
    
    saveButton = Button(root,text="Save",command=lambda: closeSaveRoot(root,filenameEntry,True),width=10).grid(row=2,column=0)
    closeButton = Button(root,text="Close",command=lambda: closeSaveRoot(root,filenameEntry,False),width=10).grid(row=2,column=1)
    
    root.mainloop()

def closeOptionsRoot(root,save,nameEntry,descriptionTextbox,unknownNameEntry,consumeDescriptionTextbox,requiredIntelligenceLevelScale,weightScale,monetaryScale,itemsStats,oldItemList):
    if save == True:
        global itemList
        itemList[0] = nameEntry.get()
        itemList[2] = descriptionTextbox.get("1.0",END)
        itemList[2] = itemList[2].replace("\n","")
        itemList[3] = unknownNameEntry.get()
        itemList[4] = consumeDescriptionTextbox.get("1.0",END)
        itemList[4] = itemList[4].replace("\n","")
        itemList[5] = requiredIntelligenceLevelScale.get()
        itemList[6] = weightScale.get()
        itemList[7] = monetaryScale.get()
        num = 8
        for i in range(len(itemsStats)):
            itemList[num] = itemsStats[i][1].get()
            num += 1

        root.destroy()

    else:
        result = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to cancel?", "Warning!", 1)
        if result == 1:
            root.destroy()

## Texture options applies stats to items e.g. gives 10 health
def textureOptions(itemList):
    root = Tk()
    root.title("Texture Options")
    root.resizable(width=False, height=False)

    Title = Label(root, text="------ Texture Options ------").grid(row=0,column=0,columnspan=4)
    
    columnWidth = 240

    itemStats = [["Health",None,-100,100],["Hunger",None,-100,100],["Fatigue",None,-100,100],["Disease",None,-100,100],["Intelligence",None,-100,100],["Strength",None,-100,100],["Luck",None,-100,100],["Charisma",None,-100,100],["Happiness",None,-100,100],["Duration",None,0,100]]

    
    ## Name
    realNameText = Message(root,text="Item's Real Name:",width = 100).grid(row=1,column=0)
    realNameEntry = Entry(root,width = 40)
    realNameEntry.insert(0, itemList[0])
    realNameEntry.grid(row=1,column=1)

    descriptionText = Message(root,text="Item Description:",width = 100).grid(row=2,column=0)
    descriptionTextbox = Text(root, height=4, width=30)
    # itemList[2] = itemList[2].replace("|","\n")
    descriptionTextbox.insert(END, itemList[2])
    descriptionTextbox.grid(row=2,column=1)

    unknownNameText = Message(root,text="Item's Unknown Name:",width = 100).grid(row=3,column=0)
    unknownNameEntry = Entry(root,width = 40)
    unknownNameEntry.insert(END, itemList[3])
    unknownNameEntry.grid(row=3,column=1)

    requiredIntelligenceLevelText = Message(root,text="Required Intelligence Level to understand name:",width = 100).grid(row=4,column=0)
    requiredIntelligenceLevelScale = Scale(root, from_=-100, to=100, orient=HORIZONTAL,length=columnWidth)
    requiredIntelligenceLevelScale.set(itemList[5])
    requiredIntelligenceLevelScale.grid(row=4,column=1)

    weightText = Message(root,text="Item Inventory Weight:",width = 100).grid(row=5,column=0)
    weightScale = Scale(root, from_=0, to=500, orient=HORIZONTAL,length=columnWidth)
    weightScale.set(itemList[6])
    weightScale.grid(row=5,column=1)

    monetaryText = Message(root,text="Monetary Value:",width = 100).grid(row=6,column=0)
    monetaryScale = Scale(root, from_=0, to=1000, orient=HORIZONTAL,length=columnWidth)
    monetaryScale.set(itemList[7])
    monetaryScale.grid(row=6,column=1)


    consumeFrame = LabelFrame(root,text="Item's Consume Stats")
    consumeFrame.grid(row=1,column=3,rowspan=10)

    consumeDescriptionText = Message(consumeFrame,text="Consume Description:",width = 100).grid(row=0,column=0)
    consumeDescriptionTextbox = Text(consumeFrame, height=4, width=30)
    # itemList[4] = itemList[4].replace("|","\n")
    consumeDescriptionTextbox.insert(END, itemList[4])
    consumeDescriptionTextbox.grid(row=0,column=1)

    x = 1
    ## Goes through item Names and creates a slider for it
    num = 8
    for eachItem in itemStats:
        text = Message(consumeFrame,text=f"{eachItem[0]}:",width = 100).grid(row=x,column=0)
        eachItem[1] = Scale(consumeFrame, from_=eachItem[2], to=eachItem[3], orient=HORIZONTAL,length=columnWidth)
        eachItem[1].set(itemList[num])
        eachItem[1].grid(row=x,column=1)
        x += 1
        num += 1
    
    ## Save and close buttton
    saveButton = Button(root,text="Save",command=lambda: closeOptionsRoot(root,True,realNameEntry,descriptionTextbox,unknownNameEntry,consumeDescriptionTextbox,requiredIntelligenceLevelScale,weightScale,monetaryScale,itemStats,itemList),width=10).grid(row=x,column=0)
    closeButton = Button(root,text="Close",command=lambda: closeOptionsRoot(root,False,realNameEntry,descriptionTextbox,unknownNameEntry,consumeDescriptionTextbox,requiredIntelligenceLevelScale,weightScale,monetaryScale,itemStats,itemList),width=10).grid(row=x,column=1)
    
    root.mainloop()





## Creates a new canvas rect
def createNewCanvasRect(win,canvasSurf,editorSurf,rectList,pixelWidth,pixelHeight,scale):
    xAdd = (win.get_width()/2-canvasSurf.get_width()/2)+editorSurf.get_width()/2
    yAdd = win.get_height()/2-canvasSurf.get_height()/2
    pixelY = 0
    for y in range(pixelHeight):
        pixelX = 0
        for x in range(pixelWidth):
            rectList[y][x][0] = pygame.Rect(xAdd+x*scale,yAdd+y*scale,scale,scale)
            pixelX += scale
        pixelY += scale
    
    return rectList

## Creates a new canvas
def createNewCanvas(win,canvasSurf,editorSurf,pixelWidth,pixelHeight,scale):
    rectList = []
    for _ in range(pixelHeight):
        rowList = []
        for _ in range(pixelWidth):
            rowList.append([None,None])
        rectList.append(rowList)
    
    rectList = createNewCanvasRect(win,canvasSurf,editorSurf,rectList,pixelWidth,pixelHeight,scale)

    return rectList

## Creates a grid for the canvas
def createGrid(rectList,win,canvasSurf,editorSurf,pixelWidth,pixelHeight,scale):
    gridSurf = pygame.Surface((canvasSurf.get_width(),canvasSurf.get_height()),pygame. SRCALPHA)

    realWidth = pixelWidth
    realHeight = pixelHeight
    
    y = 0
    for eachRow in range(realHeight):
        pygame.draw.rect(gridSurf,(45,45,45),(0,y,canvasSurf.get_width(),1))
        y += scale

    x = 0
    for eachColumn in range(realWidth):
        pygame.draw.rect(gridSurf,(45,45,45),(x,0,1,canvasSurf.get_height()))
        x += scale

    rectList = createNewCanvas(win,canvasSurf,editorSurf,pixelWidth,pixelHeight,scale)
    
    return gridSurf, rectList

## Creates a set of RGB sliders
def createRGBSliders(redValue,blueValue,greenValue):
    redValueSlider = slider(1,50,550,150,30,30,30,redValue,255,(150,100,100))

    greenValueSlider = slider(1,50,620,150,30,30,30,greenValue,255,(150,100,100))

    blueValueSlider = slider(1,50,690,150,30,30,30,blueValue,255,(150,100,100))

    return redValueSlider, greenValueSlider, blueValueSlider






while True:
    win, monitor_size = setupDisplay(1600, 900, False,"Texture Creator")
    editorSurf = pygame.Surface((300,win.get_height()))
    editorSurf.fill((100,100,100))

    canvasSurf = pygame.Surface((480,480),pygame.SRCALPHA)

    ## Display Title and other text
    title = createText(editorSurf,"Texture Creator","bahnschrift",(255,255,255),30)
    editorSurf.blit(title,(editorSurf.get_width()/2 - title.get_width()/2,0))
    title = createText(editorSurf,"__________________________","bahnschrift",(255,255,255),30)
    editorSurf.blit(title,(editorSurf.get_width()/2 - title.get_width()/2,10))

    colourValue = createText(editorSurf,"Colour Value:","bahnschrift",(255,255,255),20)
    editorSurf.blit(colourValue,(10,760))

    plus = createText(editorSurf,"+","bahnschrift",(255,255,255),20)
    editorSurf.blit(plus,(260,590))
    editorSurf.blit(plus,(260,660))

    ## Initialise Text Buttons
    newObj = textButton(win,editorSurf,1,"New Texture","bahnschrift",(255,255,255),25,10,60)
    saveObj = textButton(win,editorSurf,1,"Save Texture","bahnschrift",(255,255,255),25,10,100)
    loadObj = textButton(win,editorSurf,1,"Load Texture","bahnschrift",(255,255,255),25,10,140)
    options = textButton(win,editorSurf,1,"Texture Options","bahnschrift",(255,255,255),25,10,180)

    ## Initialise Sliders
    texturePixelWidth = 16
    texturePixelHeight = 16
    widthSlider = slider(1,50,270,200,30,30,30,texturePixelWidth,100,(150,100,100))
    heightSlider = slider(1,50,350,200,30,30,30,texturePixelHeight,100,(150,100,100))

    scale = 30
    scaleSlider = slider(1,50,430,150,30,30,30,scale,50,(150,100,100))

    redValue, greenValue, blueValue = 255,255,255
    redValueSlider, greenValueSlider, blueValueSlider = createRGBSliders(255,255,255)

    ## Initialise Colour Square Buttons
    applyScale = colourButton(1,250,430,30,30,(200,200,200),2)
    applyScale.displayButton(editorSurf,1)

    ## Initialises Grid Toggle Button
    gridToggle = colourButton(1,250,480,30,30,(200,200,200),2)
    gridToggle.displayButton(editorSurf,1)
    gridToggleText = createText(editorSurf,"Toggle Grid:","bahnschrift",(255,255,255),20)
    editorSurf.blit(gridToggleText,(10,480))
    grid = True

    ## Creating new canvas, rects for collisions and a grid
    rectList = createNewCanvas(win,canvasSurf,editorSurf,texturePixelWidth,texturePixelHeight,scale)

    gridSurf,rectList = createGrid(rectList,win,canvasSurf,editorSurf,texturePixelWidth,texturePixelHeight,scale)

    itemList = ["","","","","",0,0,0,0,0,0,0,0,0,0,0,0,0]

    drawingScreenRect = pygame.Rect(editorSurf.get_width(),0,win.get_width()-editorSurf.get_width(),win.get_height())

    clickCounter = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT: # Quites the game when pressing X
                result = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to leave?", "Warning!", 1)
                if result == 1:
                    sys.exit()
                    pygame.quit()
        
        mousePos, mousePress  = pygame.mouse.get_pos(), pygame.mouse.get_pressed() # Mouses position and press
            
        if mousePress[0] == True: # The button only activates when you click first time, not when holding button
            clickCounter += 1
        else:
            clickCounter = 0
        
        win.fill((168,63,57))

        ## Display Canvas
        win.blit(canvasSurf,((win.get_width()/2-canvasSurf.get_width()/2)+editorSurf.get_width()/2,win.get_height()/2-canvasSurf.get_height()/2))

        ## Display Grid
        if grid == True:
            win.blit(gridSurf,((win.get_width()/2-canvasSurf.get_width()/2)+editorSurf.get_width()/2,win.get_height()/2-canvasSurf.get_height()/2))

        ## Restarts the appication if a new object needs to be made
        if newObj.backButtonCollision(mousePress,mousePos,clickCounter):
            result = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to create a new texture?", "Warning!", 1)
            if result == 1:
                run = False
        
        ## Saves the Texture as a PNG file
        elif saveObj.backButtonCollision(mousePress,mousePos,clickCounter):
            if itemList[0] == "":
                ctypes.windll.user32.MessageBoxW(0, "No name assigned, go to texture options!", "Warning!", 0)
            else:
                filename = ""
                saveOptions()
                result = ctypes.windll.user32.MessageBoxW(0, f"Are you sure you want to save '{itemList[0]}' with the filename '{filename}'?", "Warning!", 1)
                if result == 1:
                    if filename != "":
                        itemList[1] = f"data/images/textures/objectLayer\{filename}.png"
                        canvasSurf = pygame.transform.scale(canvasSurf,(texturePixelWidth,texturePixelHeight))
                        pygame.image.save(canvasSurf,f"data/images/textures/objectLayer/{filename}.png")
                        canvasSurf = pygame.transform.scale(canvasSurf,(texturePixelWidth*scale,texturePixelHeight*scale))
                        itemTXT = open("data/saves/items.txt", "a")
                        itemListString = ""
                        num = 1
                        for eachItem in itemList:
                            if len(itemList) > num:
                                itemListString += f"{eachItem},"
                            else:
                                itemListString += f"{eachItem}"
                            num += 1
                            
                        itemTXT.write(f"{itemListString}|")
                        itemTXT.close()
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "No filename entered!", "Warning!", 0)
        
        ## Load new image
        elif loadObj.backButtonCollision(mousePress,mousePos,clickCounter):
            root = Tk()
            filename = askopenfilename(parent=root)
            root.destroy()
            try:
                image = pygame.image.load(filename)
                canvasSurf = pygame.transform.scale(canvasSurf,(texturePixelWidth,texturePixelHeight))
                canvasSurf.blit(image,(0,0))
                canvasSurf = pygame.transform.scale(canvasSurf,(texturePixelWidth*scale,texturePixelHeight*scale))
                print(f"Loaded '{filename}''")
            except:
                print(f"Cannot load {filename}")


        elif options.backButtonCollision(mousePress,mousePos,clickCounter):
            textureOptions(itemList)
        
        win.blit(editorSurf,(0,0))

        ## Texture Width Slider
        texturePixelWidth = widthSlider.updateSlider(win,mousePos,mousePress,1,texturePixelWidth)
        
        widthSliderText = createText(win,f"Pixel Width: {texturePixelWidth}","bahnschrift",(255,255,255),20)
        win.blit(widthSliderText,(10,240))

        ## Texture height Slider
        texturePixelHeight = heightSlider.updateSlider(win,mousePos,mousePress,1,texturePixelHeight)
        
        heightSliderText = createText(win,f"Pixel Height: {texturePixelHeight}","bahnschrift",(255,255,255),20)
        win.blit(heightSliderText,(10,320))

        ## Scale Slider
        scale = scaleSlider.updateSlider(win,mousePos,mousePress,1,scale)
        if scale < 1:
            scale = 1
        
        scaleSliderText = createText(win,f"Scale: {scale}","bahnschrift",(255,255,255),20)
        win.blit(scaleSliderText,(10,400))

        ## RGB Sliders
        redValue = redValueSlider.updateSlider(win,mousePos,mousePress,1,redValue)
        redValueText = createText(win,f"Red: {redValue}","bahnschrift",(255,255,255),20)
        win.blit(redValueText,(10,520))
        pygame.draw.rect(editorSurf,(redValue,0,0),(250,550,30,30))

        greenValue = greenValueSlider.updateSlider(win,mousePos,mousePress,1,greenValue)
        greenValueText = createText(win,f"Green: {greenValue}","bahnschrift",(255,255,255),20)
        win.blit(greenValueText,(10,590))
        pygame.draw.rect(editorSurf,(0,greenValue,0),(250,620,30,30))

        blueValue = blueValueSlider.updateSlider(win,mousePos,mousePress,1,blueValue)
        blueValueText = createText(win,f"Blue: {blueValue}","bahnschrift",(255,255,255),20)
        win.blit(blueValueText,(10,660))
        pygame.draw.rect(editorSurf,(0,0,blueValue),(250,690,30,30))

        pygame.draw.rect(editorSurf,(redValue,greenValue,blueValue),(240,750,40,40))
        
        ## Button applies the scale factor to the canvas transforming the size
        ## of the canvas, grid and rect collsions
        if applyScale.collision(mousePos,mousePress,clickCounter):
            canvasSurf = pygame.transform.scale(canvasSurf,(texturePixelWidth,texturePixelHeight))
            canvasSurf = pygame.transform.scale(canvasSurf,(texturePixelWidth*scale,texturePixelHeight*scale))
            gridSurf,rectList = createGrid(rectList,win,canvasSurf,editorSurf,texturePixelWidth,texturePixelHeight,scale)

        ## Toggles Grid
        elif gridToggle.collision(mousePos,mousePress,clickCounter):
            grid = not grid

        ## When clicking draws pixle
        if mousePress[0] == True or mousePress[2] == True:
            if drawingScreenRect.collidepoint(mousePos):
                for y in rectList:
                    for x in y:
                        if x[0].collidepoint(mousePos):
                            if mousePress[0] == True:
                                pygame.draw.rect(canvasSurf,(redValue,greenValue,blueValue),(y.index(x)*scale,rectList.index(y)*scale,scale,scale))
                                x[1] = (redValue,greenValue,blueValue)
                            else:
                                if x[1] != None:
                                    redValueSlider, greenValueSlider, blueValueSlider = createRGBSliders(x[1][0],x[1][2],x[1][1])

        pygame.display.update()