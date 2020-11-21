# from PIL import Image
import glob

def findTextures(directory):
    textureFileList = []

    for filename in glob.glob(f'{directory}*.png'):
        textureFileList.append(filename)
    
    return textureFileList