# Training pre-processing

import numpy as np
from skimage import exposure
from sklearn.preprocessing import MinMaxScaler
from osgeo import gdal

#Read input file
'''The input resulted from concatenating: i) the panchromatic (PAN) image (original #spatial resolution: 5 m)downsampled to the spatial
resolution of the HS image, which for PRISMA corresponds to 30 m; and ii) the HS image downsampled by the same ratio, i.e. 1/6 to 180 m and then 
upsampled to its original size'''

im_input=gdal.Open("Prisma_L1_input.tiff")
input_array=np.array(im_input.ReadAsArray()) 

shapein=np.shape(input_array)
rows=shapein[1]
cols=shapein[2]
bandsin=shapein[0]

'''Create new array where 1% of the histogram values for each band (left and right) are clipped to prevent lower performance 
due to sparse extreme values.'''

input_array_clip=np.uint16(np.zeros((rows,cols,bandsin)))

for i in range (bandsin):    
    p1 = np.percentile(input_array[i,:,:], 1)
    p99 = np.percentile(input_array[i,:,:], 99)      
    min_val=np.min(input_array[i,:,:])
    max_val=np.max(input_array[i,:,:])
    input_array_clip[:,:,i]= exposure.rescale_intensity(input_array[i,:,:], in_range=(p1, p99), out_range=(min_val,max_val))
    
#Reshape array of clipped values 
input_array_clip2=np.float16(np.zeros((rows*cols,bandsin)))
c=-1
for i in range(rows):
    for j in range(cols):
        c=c+1
        input_array_clip2[c,:]= input_array_clip[i,j,:]   
        
#Create array with value range [0,1] 
scaler=MinMaxScaler(feature_range = (0, 1))
input_array_scale=scaler.fit_transform(input_array_clip2)

#Reshape array of normalized values to original shape
input_arrayfin=np.float16(np.zeros((rows,cols,bandsin)))
c=-1
for i in range(rows):
    for j in range(cols):
        c=c+1
        input_arrayfin[i,j,:]=input_array_scale[c,:]
        
#Read output file: The original HS image was fed to the network as an output.
im_output=gdal.Open("Prisma_L1_output.tiff")
output_array=np.array(im_output.ReadAsArray())

shapeout=np.shape(output_array)
bandsout=shapeout[0]

'''Create new array where 1% of the histogram values for each band (left and right) are clipped to prevent lower performance 
due to sparse extreme values.'''

output_array_clip=np.uint16(np.zeros((rows,cols,bandsout)))

for i in range (bandsout):    
    p1 = np.percentile(output_array[i,:,:], 1)
    p99 = np.percentile(output_array[i,:,:], 99)    
    min_val=np.min(output_array[i,:,:])
    max_val=np.max(output_array[i,:,:])
    output_array_clip[:,:,i]= exposure.rescale_intensity(output_array[i,:,:], in_range=(p1, p99), out_range=(min_val,max_val))
    
#Reshape array of clipped values  
output_array_clip2=np.float16(np.zeros((rows*cols,bandsout)))

c=-1
for i in range(rows):
    for j in range(cols):
        c=c+1
        output_array_clip2[c,:]=output_array_clip[i,j,:]
        
#Create array with value range [0,1]     
scaler2=MinMaxScaler(feature_range = (0, 1))
output_array_scale=scaler2.fit_transform(output_array_clip2)

#Reshape array of normalized values to original shape
output_arrayfin=np.float16(np.zeros((rows,cols,bandsout)))
c=-1
for i in range(rows):
    for j in range(cols):
        c=c+1
        output_arrayfin[i,j,:]=output_array_scale[c,:]