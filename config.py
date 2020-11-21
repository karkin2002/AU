## Global variables across files

## When adding to a file remeber to type:
## import config
## config.init()

def init():     
    global stage, loadingNum, loadingRun  
    stage = 0
    loadingNum = 0
    loadingRun = True

