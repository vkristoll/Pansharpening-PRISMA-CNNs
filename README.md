# Pansharpening PRISMA images using CNNs

This repository contains code related to the pansharpening of PRISMA images by use of the PNN model (after clipping histogram values), as analyzed in the paper cited below:

Kremezi, M., Kristollari, V., Karathanassi, V., Topouzelis, K., Kolokoussis, P., Taggio, N., Aiello, A., Ceriola, G., Barbone, E. and Corradi, P., 2021. Pansharpening PRISMA Data for Marine Plastic Litter Detection Using Plastic Indexes. IEEE Access, 9, pp.61955-61971.

It can be accessed in: https://ieeexplore.ieee.org/abstract/document/9406795

![Training - Inference](/images/training_inference.png)

![Spectra](/images/Spectra.PNG)

## Steps to implement the code

Run:

>1. "read_h5_PRISMA_file.py" to read L1 PRISMA hdf5 files.
>
>2. "training_preprocessing.py" to apply pre-processing to the training input and output data. 
>
>3. "training_patches_creation.py" to create the training input and output patches.
>
>4. "model_creation_and_training.py" to create and train the PNN model.
>
>5. "inference_create_pansharpened_im.py" to make predictions and create the pansharpened image.

*Detailed guidelines are included inside each script.*

*The folder "example_image" contains a Prisma L1 level image and a .docx file with a detailed description about preparing the input files of the CNN. It also contains a .py file to georeference Prisma L2D level images.


If you use this code, please cite the below paper.

```
@article{kremezi2021pansharpening,
  title={Pansharpening PRISMA Data for Marine Plastic Litter Detection Using Plastic Indexes},
  author={Kremezi, Maria and Kristollari, Viktoria and Karathanassi, Vassilia and Topouzelis, Konstantinos and Kolokoussis, Pol and Taggio, Nicol{\`o} and Aiello, Antonello and Ceriola, Giulio and Barbone, Enrico and Corradi, Paolo},
  journal={IEEE Access},
  volume={9},
  pages={61955--61971},
  year={2021},
  publisher={IEEE}
}
```




























