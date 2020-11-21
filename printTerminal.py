import time

def printTerminal(typeMsg,msg):
    timeString = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{typeMsg}] {timeString}: {msg}")