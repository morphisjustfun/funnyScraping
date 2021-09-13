import os
import sys
import numpy as np
import subprocess
import random

os.system('convert captcha.png -crop 4@x1 CROP-%d.jpg')

dicTotal = {}

for i in range(4):
    subDic = {}
    for k in range(50, 100, int(sys.argv[1])):
        os.system(
            f'convert CROP-{i}.jpg -colorspace Gray -blur 0 -level 0,{k}% test1.jpg')
        result = subprocess.check_output(
            ['tesseract', '-c', 'tessedit_char_whitelist=0123456789', '--psm', '7', 'test1.jpg', '-'])
        result = result.decode('utf-8')
        result = result.strip()
        if result != '':
            if result in subDic.keys():
                subDic[result] = subDic[result] + 1
            else:
                subDic[result] = 1
    if len(subDic) == 0:
        print("No coincidence")
        exit(1)
    dicTotal[i] = subDic

storedMax = []

for i in dicTotal.keys():
    allValues = dicTotal[i].values()
    # print(np.std(list(allValues)))
    maxLocal = max(allValues)
    maxLocals = []
    for j in dicTotal[i].keys():
        if dicTotal[i][j] == maxLocal:
            maxLocals.append(j)
    storedMax.append(random.choice(maxLocals))


captcha = ''.join(str(item) for item in storedMax)
print(captcha)
