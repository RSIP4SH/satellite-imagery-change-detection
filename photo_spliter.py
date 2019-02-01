import image_slicer

def slice_image(image_path, slice_numbers, output_path):
    tiles = image_slicer.slice(image_path, slice_numbers, save=False)
    image_slicer.save_tiles(tiles, directory=output_path, prefix='slice')
    return tiles
