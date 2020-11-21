from chunkClass import chunk
from printTerminal import printTerminal


def openItems():
    ## Opens a txt file with all the item data
    ## stored on it and splits it into an array
    noteItems = open("data/saves/items.txt", "r")
    itemList = noteItems.read().split('|')
    
    tempItem  = []
    
    for eachItem in range(len(itemList)-1):
        tempItem.append([itemList[eachItem]])

    items = []
    for i in tempItem:
        items.append(i[0].split(','))
    
    return items


def openMapArray(mapName):
    mapArrayTxt = open(f"data/saves/{mapName}.txt", "r")
    mapArraY = mapArrayTxt.read().splitlines()

    tempItem  = []
    
    for eachItem in mapArraY:
        tempItem.append([eachItem])

    items = []
    for i in tempItem:
        items.append(i[0].split('|'))
    
    numY = 0
    for y in items:
        numX = 0
        for x in y:
            
            # if numX < len(items[0])-1:
                
            tempX = x.split(",")
            for eachSection in tempX:
                if eachSection == "False":
                    tempX[tempX.index(eachSection)] = False
                elif eachSection == "True":
                    tempX[tempX.index(eachSection)] = True
                elif eachSection == "None":
                    tempX[tempX.index(eachSection)] = None
                
                items[numY][numX] = chunk(tempX[0],tempX[1],tempX[2],tempX[3])
            
            numX += 1
        numY += 1
    
    mapArrayTxt.close()
    
    try:
        mapDataTxt = open(f"data/saves/{mapName}Data.txt", "r")
        mapData = mapDataTxt.read()
        gridRef = mapData.split(",")
        gridRef[0], gridRef[1] = int(gridRef[0]), int(gridRef[1])
        mapDataTxt.close()
    
    except:
        printTerminal("Info",f"Created new textfile {mapName}Data")
        mapDataTxt = open(f"data/saves/{mapName}Data.txt", "w")
        mapDataTxt.write("0,0")
        mapDataTxt.close()
        gridRef = [0,0]
    
    return items, gridRef
