import os.path
import re
import requests

import PIL
from PIL import Image

DATADIR = "D:/kkya5/Pictures/Datasets/Pokemon"
CATEGORIES = os.listdir(DATADIR)

NEWDATADIR = "D:/kkya5/Pictures/Datasets/PokemonGame"

for i in CATEGORIES:
    addy = ""
    i = i.lower()

    if("nidoran" in i):
        if("f" in i):
            i = "nidoran-f"
        else:
            i = "nidoran-m"
    elif("mime" in i):
        i = "mr-mime"
    elif("farfet" in i):
        i = "farfetchd"
    newFolder = NEWDATADIR+"/"+i
    os.mkdir(newFolder)

    URL = "https://pokemondb.net/sprites/"+i
    r = requests.get(URL)
    text = r.text
    httpArr = [m.start() for m in re.finditer('https://', text)]
    pngArr = [m.start() for m in re.finditer(".png", text)]
    pngIndex = 0
    urlArr = []
    for j in httpArr:
        nextHttp = httpArr.index(j)+1
        try:
            if(nextHttp >= len(httpArr) and pngIndex >= len(pngIndex)):
                break
            elif(pngArr[pngIndex] < httpArr[nextHttp]):
                imgUrl = text[j:pngArr[pngIndex]+4]
                try:
                    meme = imgUrl.index(
                        i) != -1 and imgUrl.index(">") == -1 and imgUrl.index("<") == -1
                except Exception as e:
                    if("back" not in imgUrl and imgUrl not in urlArr):
                        urlArr.append(imgUrl)
                    else:
                        print("back!")
                pngIndex += 1
        except Exception as f:
            print(":(")
    for j in urlArr:
        response = requests.get(j)
        if(response.status_code == 200):
            with open(NEWDATADIR+"/"+i+"/"+str(urlArr.index(j))+".png", "wb") as f:
                f.write(response.content)
