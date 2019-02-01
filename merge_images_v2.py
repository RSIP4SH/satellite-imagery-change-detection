from PIL import Image
from photo_spliter import slice_image
from math import sqrt

def merge_chunks(list_of_chunks, number_of_chunks, original_size):

	list_index = [j for i in range(int(sqrt(number_of_chunks))) for j in range(i, number_of_chunks, int(sqrt(number_of_chunks)))]

	new_im = Image.new('RGB', original_size)

	index = 0
	for i in range(0, original_size[0], original_size[0]//int(sqrt(number_of_chunks))+1):
		for j in range(0, original_size[1], original_size[1]//int(sqrt(number_of_chunks))+1):
		    im = Image.open(list_of_chunks[list_index[index]])
		    new_im.paste(im, (i,j))
		    index += 1

	new_im.save('test.jpg')

#merge_chunks(list_im, 9, (1877, 899))
