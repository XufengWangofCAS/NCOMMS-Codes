from gdalconst import *
from osgeo import osr
import gdal
def ReadGeoTiff(inputfile):
    ds = gdal.Open(inputfile)
    band = ds.GetRasterBand(1)
    data_arr = band.ReadAsArray()
    [Ysize, Xsize] = data_arr.shape
    return data_arr, Ysize, Xsize

def GetGeoInfo(FileName):
    SourceDS = gdal.Open(FileName, GA_ReadOnly)
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())    
    return GeoT, Projection

def CreateGeoTiff(Name, Array, xsize, ysize, GeoT, Projection,NoData_value):
    
    gdal.AllRegister()
    driver = gdal.GetDriverByName('GTiff')
    DataType = gdal.GDT_Float32
    NewFileName = Name+'.tif'
    # Set up the dataset
    DataSet = driver.Create( NewFileName, xsize, ysize, 1, DataType )
            # the '1' is for band 1.
    DataSet.SetGeoTransform(GeoT)
    DataSet.SetProjection( Projection.ExportToWkt() )
    # Write the array
    DataSet.GetRasterBand(1).WriteArray( Array )
    
    outBand = DataSet.GetRasterBand(1)
    # flush data to disk, set the NoData value and calculate stats
    outBand.FlushCache()
    outBand.SetNoDataValue(NoData_value)
    return NewFileName