#Create pansharpened PRISMA image

#Load the previously saved weights from the training
#model is defined in model_creation.py
model.load_weights("weights.h5") 

from osgeo import gdal
import numpy as np

#bandsin, input_array, exposure, scaler, bandsout, scaler2 are explained in training_preprocessing.py

'''
During the inference stage, the pan-sharpened image (spatial resolution: 5 m) was created by feeding the network with an input that results from concatenating: i) the original
PAN image; and ii) the original HS image upsampled to the size of the original PAN. '''

im_test=gdal.Open("Prisma_L1_input_inference.tiff")
im_test_array=np.array(im_test.ReadAsArray()) 

shapetest=np.shape(im_test_array)
rowstest=shapetest[1]
colstest=shapetest[2]

'''Create new array where 1% of the histogram values for each band (left and right) are clipped to prevent lower performance 
due to sparse extreme values.'''
input_array_test_clip=np.uint16(np.zeros((rowstest,colstest,bandsin)))
for i in range (bandsin):
    # The histogram values of the training input image are used (input_array)
    p1 = np.percentile(input_array[i,:,:], 1)
    p99 = np.percentile(input_array[i,:,:], 99)    
    min_val=np.min(input_array[i,:,:])
    max_val=np.max(input_array[i,:,:])
    input_test_array_clip[:,:,i]= exposure.rescale_intensity(im_test_array[i,:,:], in_range=(p1, p99), out_range=(min_val,max_val))

#Reshape array of clipped values     
input_test_array_clip2=np.float16(np.zeros((rowstest*colstest,bandsin)))
c=-1
for i in range(rowstest):
    for j in range(colstest):
        c=c+1
        input_test_array_clip2[c,:]=input_test_array_clip[i,j,:]

#Create array with value range [0,1]. The scaling is performed according to the values of the training image
input_test_array_scale=scaler.transform(input_test_array_clip2)

#Reshape array of normalized values to original shape
input_testarrayfin=np.float16(np.zeros((rowstest,colstest,bandsin)))
c=-1
for i in range(rowstest):
    for j in range(colstest):
        c=c+1
        input_testarrayfin[i,j,:]=input_test_array_scale[c,:]

#Create patches and make predictions
#The patch size is 9x9. rowstest, colstest are divided by 9 without remainder.        
a=int(colstest/9)
b=int(rowstest/9)

#Create empty list to store predictions
l=[]

X= np.zeros((a,9,9,bandsin))
c=-1
for i in range(0,rowstest,9):    
    print(" The repetition number is %s" %i)     
    for j in range(0,colstest,9):
        c=c+1
        # X stores predictions equal to int(colstest/9)
        X[c-1,:,:,:]= input_testarrayfin[i:i+9,j:j+9,:]
    c=0
    predictions=model.predict(X)
    l.append(predictions)
  
#Create the output pansharpened image  
pansharpened=np.float16(np.zeros((rowstest,colstest,bandsout)))
for i in range(b):
    for j in range (a):
        pansharpened[i*9:i*9+9,j*9:j*9+9,:]=l[i][j]
        
#Remove the 0-1 scaling transformation to recover uint16 values       
pansharpened_recovered1=np.float16(np.zeros((rowstest*colstest,bandsout)))
c=-1
for i in range(rowstest):
    for j in range(colstest):
        c=c+1
        pansharpened_recovered[c,:]=pansharpened[i,j,:]    
        
pansharpened_recovered1= scaler2.inverse_transform(pansharpened_recovered1)   

#Reshape to the output image shape
pansharpened_recovered2=np.float16(np.zeros((rowstest,colstest,bandsout)))
c=-1
for i in range(rowstest):
    for j in range(colstest):
        c=c+1
        pansharpened_recovered2[i,j,:]=pansharpened_recovered1[c,:]    
       
#Save pansharpened image  
target_layer="pansharpened.tiff"     
driver= gdal.GetDriverByName('GTiff')    
target_ds = driver.Create(target_layer, colstest, rowstest, bands=bandsout, eType=gdal.GDT_UInt16)        
    
for i in range(bandsout):
            
    outBand = target_ds.GetRasterBand(i+1)
    outBand.WriteArray(pansharpened_recovered2[:,:,i])

target_ds= None
