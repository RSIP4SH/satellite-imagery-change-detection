from PIL import Image
import numpy as np

def merge(img1, img2):

	img2 = img2.resize(img1.size)

	image = img2.convert('RGBA')
	datas = image.getdata()
	newData = []
	for item in datas:
		if item[0] == 255 and item[1] == 255 and item[2] == 255:
		    newData.append((255,255,255,0))
		else:
		    newData.append(item)
	image.putdata(newData)
	img2 = image

	img1.paste(img2, mask=img2)

	return img1
