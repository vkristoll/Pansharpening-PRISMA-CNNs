#Read PRISMA L1 hdf5 file

import h5py
import numpy as np


# Read hdf5 file
PRISMA_L1_file_path = "PRS_L1_STD_OFFL_etc.he5"
PRISMA_L1_file= h5py.File(PRISMA_L1_file_path, 'r') 

#Read PAN data
PRISMA_PAN = PRISMA_L1_file.get('HDFEOS/SWATHS/PRS_L1_PCO/Data Fields/Cube')
PRISMA_PAN_array = np.array(PRISMA_PAN)    
PRISMA_PAN_rot=np.rot90(PRISMA_PAN_array,k=3) 

#Read VNIR data
PRISMA_VNIR= PRISMA_L1_file.get('HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/VNIR_Cube') 
PRISMA_VNIR_correct_order = np.array(PRISMA_VNIR)[:, ::-1, :]
PRISMA_VNIR_rot=np.rot90(PRISMA_VNIR_correct_order,k=3, axes=(0, 2))

#Read SWIR data
PRISMA_SWIR = PRISMA_L1_file.get('HDFEOS/SWATHS/PRS_L1_HCO/Data Fields/SWIR_Cube')
PRISMA_SWIR_correct_order= np.array(PRISMA_SWIR)[:, ::-1, :]
PRISMA_SWIR_rot=np.rot90(PRISMA_SWIR_correct_order,k=3, axes=(0, 2))

