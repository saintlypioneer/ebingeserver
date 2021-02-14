import os
from PIL import Image
for file in os.listdir(os.getcwd()):
    if file.split(".")[-1]=='jpg':
        pic = Image.open(file)
        pic.save("C"+file, "JPEG", optimise=True, quality=10)
        pic.close()
        os.remove(file)
        os.rename("C"+file, file)
