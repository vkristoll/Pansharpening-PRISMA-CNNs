#Create input and output arrays of training patches

#input_arrayfin, output_arrayfin, rows, cols, bandsin are explained in training_preprocessing.py

import math
import numpy as np


def create_patches(output_arrayfin, input_arrayfin, input_patch_xysize, bandsin):
     
     #calculate size of padded image (it should be divided with the input_patch_xysize without remainder)   
     y_size=(math.floor(rows/input_patch_xysize) + 1) * input_patch_xysize
     x_size=(math.floor(cols/input_patch_xysize) + 1) * input_patch_xysize
     
     y_pad= int(y_size - rows)     
     x_pad= int(x_size - cols)
    
     #create padded  input and output images
     input_arraypad=np.float16(np.zeros((rows+y_pad, cols+x_pad, bandsin)))    
     input_arraypad[0:rows,0:cols,:]=input_arrayfin
     
     output_arraypad=np.float16(np.zeros((rows+y_pad, cols+x_pad, bandsin-1)))    
     output_arraypad[0:rows,0:cols,:]=output_arrayfin
     
     #create input and output training patches
     input_list_patches=[]
     output_list_patches=[]     
     
     for i in range(0, y_size-input_patch_xysize, 4): #~50% overlap
        for j in range(0, x_size-input_patch_xysize, 4):
            input_list_patches.append(input_arraypad[i:i+input_patch_xysize, j:j+input_patch_xysize,:])
            output_list_patches.append(output_arraypad[i:i+input_patch_xysize, j:j+input_patch_xysize,:])
     
     input_patches=np.zeros((len(input_list_patches),input_patch_xysize,input_patch_xysize,bandsin))
     output_patches=np.zeros((len(output_list_patches),input_patch_xysize,input_patch_xysize,bandsin-1))
     
     for i in range (len(input_list_patches)):
        input_patches[i,:,:,:] = input_list_patches[i]
        output_patches[i,:,:,:] = output_list_patches[i]   
    
     return input_patches, output_patches
    

#use the function
input_patch_xysize=9
[x,y]=create_patches(output_arrayfin,input_arrayfin, input_patch_xysize, bandsin)   


