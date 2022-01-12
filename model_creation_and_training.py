#Model creation - training

#PNN model

''' This script implements the architecture described in 
'Pansharpening by Convolutional Neural Networks' by Masi G., Cozzolino D., Verdoliva L., Scarpa G. (2016) 
See also https://github.com/ThomasWangWeiHong/Pansharpening-by-Convolutional-Neural-Network'''

from keras.models import Input, Model
from keras.layers import Conv2D
from keras.optimizers import Adam

#input_patch_xysize, bandsin are explained in training_preprocessing.py, and x,y in training_patches_creation.py

def PNN_model(input_patch_xysize,bandsin):
    
    img_input = Input(shape = (input_patch_xysize, input_patch_xysize, bandsin))
    conv1 = Conv2D(64, (9, 9), activation = 'relu',padding = 'same')(img_input)
    conv2 = Conv2D(32, (5, 5), activation = 'relu', padding = 'same')(conv1)
    conv3 = Conv2D(bandsin-1, (5, 5),activation = 'sigmoid', padding = 'same')(conv2)
    
    model = Model(inputs = img_input, outputs = conv3)
    model.compile(optimizer = Adam(lr = 0.0001), loss = 'mse', metrics = ['mse'])   

    return model
    

#train the model
model=PNN_model(input_patch_xysize,bandsin)
model.fit(x,y,epochs=160, batch_size =128) 

model.save_weights("weights.h5")
