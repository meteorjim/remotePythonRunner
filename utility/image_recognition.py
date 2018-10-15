from PIL import Image
import pytesseract


def _binarizing(img,threshold): #input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def _depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img

def img_varification_to_string(img_path,threshold):
    target_image = Image.open(img_path)
    target_image = target_image.convert('L')
    target_image = _binarizing(target_image,100)
    target_image = _depoint(target_image)
    target_image.save('./temp_img/reconition.png')
    validate_str = pytesseract.image_to_string(target_image,config='-psm 7')
    return validate_str

