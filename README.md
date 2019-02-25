# satellite-imagery-change-detection
Detect unstructured changes in satellite images

This program detect changes in satellite(maybe any other) image using deep learning ResNet50 architecture.

#### Usage: python3 detectUI.py 

requirements:
- pyqt5
- keras
- numpy
- image_slicer
- scikit-image

Original image:
![link](https://github.com/soroushhashemifar/satellite-imagery-change-detection/blob/master/sen2_2018_dataset_bm1_qua_bm2.jpg)

Target image:
![link](https://github.com/soroushhashemifar/satellite-imagery-change-detection/blob/master/sen2_2018_dataset_bm1_qua_bm2_2.jpg)

Changes applied to target image:
![link](https://github.com/soroushhashemifar/satellite-imagery-change-detection/blob/master/sen2_2018_dataset_bm1_qua_bm2_2_new.jpg)

Output of algorithm:
![link](https://github.com/soroushhashemifar/satellite-imagery-change-detection/blob/master/test.jpg)
