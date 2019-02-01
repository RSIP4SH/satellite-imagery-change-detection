from feat import main
import numpy as np
from photo_spliter import slice_image
from image_slicer import join, Tile
from merge_images_v2 import merge_chunks
import matplotlib.pyplot as plt
import os
from PIL import Image
import sys
from math import sqrt
import time
import gc

NUMBER_OF_SLICES = 9

slices_of_img1 = list(slice_image(sys.argv[1], NUMBER_OF_SLICES, 'slices_of_img1'))
slices_of_img2 = list(slice_image(sys.argv[2], NUMBER_OF_SLICES, 'slices_of_img2'))

orig_size = Image.open(sys.argv[1]).size

start = time.time()
slice_index = 1
for img1, img2 in zip(slices_of_img1, slices_of_img2):
	output_photo = main(img1.filename, img2.filename, orig_size, slice_index)
	im = Image.fromarray(np.array(output_photo))
	im = im.resize((orig_size[0] // int(sqrt(NUMBER_OF_SLICES)), orig_size[1] // int(sqrt(NUMBER_OF_SLICES))), Image.ANTIALIAS)
	im.save(img1.filename)
	print('slice [{}/{}] processed'.format(slice_index, NUMBER_OF_SLICES))
	slice_index += 1
	gc.collect()

print("time elapsed: {}".format(time.time() - start))
merge_chunks([filename.filename for filename in slices_of_img1], NUMBER_OF_SLICES, orig_size)
