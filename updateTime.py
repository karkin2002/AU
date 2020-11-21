import time

def updateTime(last_time):
    dt = time.time() - last_time # Checks how much time passed dt = delta time
    dt *= 60 # One second passing == 60 frames
    last_time = time.time()
    return dt, last_time