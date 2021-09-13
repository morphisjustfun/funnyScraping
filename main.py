import http.client
import json
import random
import string
import os
from PIL import Image

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def p(img, letter):
    A = img.load()
    B = letter.load()
    mx = 1000000
    max_x = 0
    x = 0
    for x in range(img.size[0] - letter.size[0]):
        _sum = 0
        for i in range(letter.size[0]):
            for j in range(letter.size[1]):
                _sum = _sum + abs(A[x+i, j][0] - B[i, j][0])
        if _sum < mx :
            mx = _sum
            max_x = x
    return mx, max_x

def ocr(im, threshold=200, alphabet="0123456789abcdef"):
    img = Image.open(im)
    img = img.convert("RGB")
    box = (8, 8, 58, 18)
    img = img.crop(box)
    pixdata = img.load()

    letters = Image.open('letters.bmp')
    ledata = letters.load()

    # Clean the background noise, if color != white, then set to black.
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (pixdata[x, y][0] > threshold) \
                    and (pixdata[x, y][1] > threshold) \
                    and (pixdata[x, y][2] > threshold):

                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)

    counter = 0;
    old_x = -1;

    letterlist = []

    for x in range(letters.size[0]):
        black = True
        for y in range(letters.size[1]):
            if ledata[x, y][0] != 0 :
                black = False
                break
        if black :
            if True :
                box = (old_x + 1, 0, x, 10)
                letter = letters.crop(box)
                t = p(img, letter);
                print (counter, x, t)
                letterlist.append((t[0], alphabet[counter], t[1]))
            old_x = x
            counter += 1

    box = (old_x + 1, 0, 140, 10)
    letter = letters.crop(box)
    t = p(img, letter)
    letterlist.append((t[0], alphabet[counter], t[1]))

    t = sorted(letterlist)
    t = t[0:5]  # 5-letter captcha

    final = sorted(t, key=lambda e: e[2])
    answer = ""
    for l in final:
        answer = answer + l[1]
    return answer

def decoder(
        im,
        threshold=200,
        mask="letters.bmp",
        alphabet="0123456789abcdef"):

    img = Image.open(im)
    img = img.convert("RGB")
    box = (8, 8, 58, 18)
    img = img.crop(box)
    pixdata = img.load()

    # open the mask
    letters = Image.open(mask)
    ledata = letters.load()

    def test_letter(img, letter):
        A = img.load()
        B = letter.load()
        mx = 1000000
        max_x = 0
        x = 0
        for x in range(img.size[0] - letter.size[0]):
            _sum = 0
            for i in range(letter.size[0]):
                for j in range(letter.size[1]):
                    _sum = _sum + abs(A[x + i, j][0] - B[i, j][0])
            if _sum < mx:
                mx = _sum
                max_x = x
        return mx, max_x

    # Clean the background noise, if color != white, then set to black.
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (pixdata[x, y][0] > threshold) \
                    and (pixdata[x, y][1] > threshold) \
                    and (pixdata[x, y][2] > threshold):

                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)

    counter = 0
    old_x = -1

    letterlist = []

    for x in range(letters.size[0]):
        black = True
        for y in range(letters.size[1]):
            if ledata[x, y][0] != 0:
                black = False
                break
        if black:
            box = (old_x + 1, 0, x, 10)
            letter = letters.crop(box)
            t = test_letter(img, letter)
            letterlist.append((t[0], alphabet[counter], t[1]))
            old_x = x
            counter += 1

    box = (old_x + 1, 0, 140, 10)
    letter = letters.crop(box)
    t = test_letter(img, letter)
    letterlist.append((t[0], alphabet[counter], t[1]))

    t = sorted(letterlist)
    t = t[0:4]  # 5-letter captcha

    final = sorted(t, key=lambda e: e[2])

    answer = ''.join(map(lambda l: l[1], final))
    return answer


# conn = http.client.HTTPSConnection("consultas-api.pongoelhombro.gob.pe")
# payload = "{\"documento\":\"72683851\",\"tipoDocumento\":\"1\",\"nacionalidad\":\"\"}"
# headers = {
#   'GAction': 'xyf1f9c1-302a-4d04-am32-d40mm0f409bx',
#   'Accept': 'application/json, text/plain, */*',
#   'Content-Type': 'application/json',
#   'GResponse': '5305',
#   'sec-ch-ua-mobile': '?0',
#   'origin':'https://consultas.pongoelhombro.gob.pe',
#   'referer':"https://consultas.pongoelhombro.gob.pe/",
#   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
#   'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90"'
# }
# conn.request("POST", "/ciudadano", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8")

randomCode = f'{get_random_string(8)}-{get_random_string(4)}-{get_random_string(4)}-{get_random_string(4)}-{get_random_string(12)}'


conn = http.client.HTTPSConnection("consultas-api.pongoelhombro.gob.pe")
payload = ''
headers = {
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90"',
  'sec-ch-ua-mobile': '?0',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
conn.request("GET", f'/captcha/{randomCode}', payload, headers)
res = conn.getresponse()
if res.status == 200:
    data = res.read()
    decoded = data.decode('utf-8')
    #decoded = decoded.replace("\\",'')
    svg = json.loads(decoded)
    fileSVG = open('captcha.svg','w')
    fileSVG.write(svg['image'])
    fileSVG.close()

    convertCode = os.system('convert captcha.svg captcha.png')
    if convertCode == 0:
        # print(decoder('captcha.png')
        print(randomCode)
