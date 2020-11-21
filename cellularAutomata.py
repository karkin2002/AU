from chunkClass import *

## Goes through a map array and for each texture
## if it has 4 or more different textures around it
## it becomes that texture otherwise it stays as
## it's original texture, this creates an island
## effect
def cellularAutomata(mapArray,passes):
    for _ in range(passes): # Pass through the algorithm to smooth map
        
        numy = 0
        for y in mapArray: # For each row in the map
            numx = 0
            
            for x in y: # For each item in each row
                surrounding = [] # List of the textures surrounding the item we're looking at
                
                if numx != 0: # Validation to make sure it's not on the edge
                    surrounding.append(mapArray[numy][numx-1].texture)

                if numx != len(mapArray[numy])-1:
                        surrounding.append(mapArray[numy][numx+1].texture)

                if numy != 0:
                    surrounding.append(mapArray[numy-1][numx].texture)
                    
                    if numx != 0:
                        surrounding.append(mapArray[numy-1][numx-1].texture)
                    
                    if numx != len(mapArray[numy])-1:
                        surrounding.append(mapArray[numy-1][numx+1].texture)
                
                if numy != len(mapArray)-1:
                    surrounding.append(mapArray[numy+1][numx].texture)
                    
                    if numx != 0:
                        surrounding.append(mapArray[numy+1][numx-1].texture)
                    
                    if numx != len(mapArray[0])-1:
                        surrounding.append(mapArray[numy+1][numx+1].texture)
                
                surroundingFound = []
                for eachItem in surrounding:
                    if eachItem not in surroundingFound:
                        surroundingFound.append(eachItem)
                
                surroundingNum = []
                for eachItem in surroundingFound:
                    surroundingNum.append([eachItem,surrounding.count(eachItem)]) # Counts how many of each texture are in the surrounding list

                ## Gets the texture that is highest occusring, if it
                ## is greate than 4 it replaces the items texture with
                ## the highest occuring texture
                highestOccurance = surroundingNum[0]
                for eachItem in surroundingNum:
                    if eachItem[1] > highestOccurance[1]:
                        highestOccurance = eachItem
                
                if highestOccurance[1] > 4:
                    x.texture = highestOccurance[0]


                numx += 1
            
            numy += 1

        return mapArray