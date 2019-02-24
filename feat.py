import tensorflow as tf
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import numpy as np
import sys
from skimage import filters
from keras import backend as K
from merge_images import merge
from PIL import Image
import scipy.misc

x = 100
RESIZE_SIZE = [0,0]

#Function to retrieve features from intermediate layers
def get_activations(model, layer_idx, X_batch):
    get_activations = K.function([model.layers[0].input, K.learning_phase()], [model.layers[layer_idx].output,])
    activations = get_activations([X_batch,0])
    return activations

#Function to extract features from intermediate layers
def extra_feat(img_path):
    #Using a RESNET50 as feature extractor
    base_model = ResNet50(weights='imagenet',include_top=False)
    img = image.load_img(img_path, target_size=RESIZE_SIZE)
    x_img = image.img_to_array(img)
    x = np.expand_dims(x_img, axis=0)
    x = preprocess_input(x)
    block1_pool_features=get_activations(base_model, 10, x)
    block2_pool_features=get_activations(base_model, 15, x)
    block3_pool_features=get_activations(base_model, 17, x)
    #block4_pool_features=get_activations(base_model, 20, x)
    block5_pool_features=get_activations(base_model, 22, x)
    #block6_pool_features=get_activations(base_model, 25, x)
    block7_pool_features=get_activations(base_model, 30, x)
    #block8_pool_features=get_activations(base_model, 35, x)
    block9_pool_features=get_activations(base_model, 37, x)
    #block10_pool_features=get_activations(base_model, 39, x)
    block11_pool_features=get_activations(base_model, 42, x)
    #block12_pool_features=get_activations(base_model, 45, x)
    block13_pool_features=get_activations(base_model, 46, x)
    block14_pool_features=get_activations(base_model, 47, x)
    block15_pool_features=get_activations(base_model, 50, x)
    #block16_pool_features=get_activations(base_model, 23, x)
    block17_pool_features=get_activations(base_model, 27, x)
    block18_pool_features=get_activations(base_model, 33, x)
    #block19_pool_features=get_activations(base_model, 38, x)
    block20_pool_features=get_activations(base_model, 43, x)
    block21_pool_features=get_activations(base_model, 49, x)

    x1 = tf.image.resize_images(block1_pool_features[0],RESIZE_SIZE)
    x2 = tf.image.resize_images(block2_pool_features[0],RESIZE_SIZE)
    x3 = tf.image.resize_images(block3_pool_features[0],RESIZE_SIZE)
    #x4 = tf.image.resize_images(block4_pool_features[0],RESIZE_SIZE)
    x5 = tf.image.resize_images(block5_pool_features[0],RESIZE_SIZE)
    #x6 = tf.image.resize_images(block6_pool_features[0],RESIZE_SIZE)
    x7 = tf.image.resize_images(block7_pool_features[0],RESIZE_SIZE)
    #x8 = tf.image.resize_images(block8_pool_features[0],RESIZE_SIZE)
    x9 = tf.image.resize_images(block9_pool_features[0],RESIZE_SIZE)
    #x10 = tf.image.resize_images(block10_pool_features[0],RESIZE_SIZE)
    x11 = tf.image.resize_images(block11_pool_features[0],RESIZE_SIZE)
    #x12 = tf.image.resize_images(block12_pool_features[0],RESIZE_SIZE)
    x13 = tf.image.resize_images(block13_pool_features[0],RESIZE_SIZE)
    x14 = tf.image.resize_images(block14_pool_features[0],RESIZE_SIZE)
    x15 = tf.image.resize_images(block15_pool_features[0],RESIZE_SIZE)
    #x16 = tf.image.resize_images(block16_pool_features[0],RESIZE_SIZE)
    x17 = tf.image.resize_images(block17_pool_features[0],RESIZE_SIZE)
    x18 = tf.image.resize_images(block18_pool_features[0],RESIZE_SIZE)
    #x19 = tf.image.resize_images(block19_pool_features[0],RESIZE_SIZE)
    x20 = tf.image.resize_images(block20_pool_features[0],RESIZE_SIZE)
    x21 = tf.image.resize_images(block21_pool_features[0],RESIZE_SIZE)

    F = tf.concat([x1,x2,x3,x5,x7,x9,x11,x13,x14,x15,x17,x18,x20,x21], 3)
    return F, x_img

def main(img_path1, img_path2, original_size, index, result_path=""):

    global RESIZE_SIZE, x
    RESIZE_SIZE = [x, x*original_size[0]//original_size[1]]

    sess = tf.InteractiveSession()

    F1, img1=extra_feat(img_path1) #Features from image patch 1
    F1=tf.square(F1)
    F2, img2=extra_feat(img_path2) #Features from image patch 2
    F2=tf.square(F2)
    d=tf.subtract(F1,F2)
    d=tf.square(d)
    d=tf.reduce_sum(d,axis=3)

    dis=(d.eval())   #The change map formed showing change at each pixels
    dis=np.resize(dis,RESIZE_SIZE)

    try:
        val = filters.threshold_otsu(dis[:,:])

        output_photo = dis[:,:] < val
        output_photo = np.array(output_photo).astype(int) * 255

    except:
        output_photo = np.ones((RESIZE_SIZE[0],RESIZE_SIZE[1],3)) * 255
    
    tf.InteractiveSession.close(sess)

    result = Image.fromarray(output_photo.astype(np.uint8))
    result.save('__temp__/_foreground_{}.png'.format(index))
    scipy.misc.imsave('__temp__/_background_{}.png'.format(index), img1)
    output_photo = merge(Image.open('__temp__/_background_{}.png'.format(index)), Image.open('__temp__/_foreground_{}.png'.format(index)))

    return output_photo

if __name__ == "__main__":
    if (len(sys.argv))>3:
        print("Invalid number of input arguments ")
        exit(0)

    main(sys.argv[1], sys.argv[2])
