'''Guidelines to include georeference PRISMA L2D image. L1 images do not contain georeference information, thus they can be manually georeferenced 
in a GIS tool by use of a basemap or the L2D corresponding image.'''

import h5py
import numpy as np
from osgeo import osr, gdal

# Read hdf5 file
PRISMA_L2D_file_path = "PRS_L2D_STD_OFFL_etc.he5"
PRISMA_L2D_file= h5py.File(PRISMA_L2D_file_path, 'r') 

#Read PAN data
PRISMA_PAN = PRISMA_L2D_file.get('HDFEOS/SWATHS/PRS_L2D_PCO/Data Fields/Cube')
PRISMA_PAN_array = np.array(PRISMA_PAN)    

'''By using gdalinfo in the console for a PRISMA Level 2D image, ULcorner_northing,  ULcorner_easting,  LRcorner_northing, 
LRcorner_easting and Epsg_Code can be found.'''

rasterOrigin = [UL_easting, UL_northing]
PAN_pixelWidth = (LR_easting - UL_easting) / PRISMA_PAN_array.shape[1]
PAN_pixelHeight = (UL_northing - LR_northing) / PRISMA_PAN_array.shape[0]
PAN_pixelSize = [PAN_pixelWidth, PAN_pixelHeight]

def savemap(fname_tif_out_PAN, array, format, rasterOrigin, pixelSize, Epsg_Code, data_type = gdal.GDT_UInt16):
    if len(array.shape) == 2:
        array = np.expand_dims(array, axis=1)

    rows = array.shape[0]
    bands = array.shape[1]
    cols = array.shape[2]

    originX = rasterOrigin[0]
    originY = rasterOrigin[1]
    pixelWidth = pixelSize[0]
    pixelHeight = pixelSize[1]

    driver = gdal.GetDriverByName(format)
    outRaster = driver.Create(fname_tif_out_PAN, cols, rows, bands, data_type)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, -pixelHeight))

    for band in range(bands):
        outRaster.GetRasterBand(band + 1).WriteArray(array[:, band, :])
        outRaster.GetRasterBand(band + 1).FlushCache()

    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(Epsg_Code)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())

fname_tif_out_PAN="PRISMA_PAN_L2D_map.tiff"

savemap(fname_tif_out_PAN, PRISMA_PAN_array, 'GTiff', rasterOrigin, PAN_pixelSize, Epsg_Code)
