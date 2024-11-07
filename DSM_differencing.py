import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from rasterio.plot import plotting_extent

#preparing the rasters

DSM_path1 = r"C:\Team_Shrub\LabData\CameronData\MME_OdeheadRidge_70m_13Aug2024\OdeheadRidge13Aug202470m20240814-DEM.tif" #example from Cameron
DSM_path2 = r"C:\Team_Shrub\LabData\CameronData\MME_OdeheadRidge_70m_12Aug2024\OdeheadRidge12Aug202470m20240814-DEM.tif"

with rio.open(DSM_path1) as DSM_src:
    DSM1 = DSM_src.read(1)

with rio.open(DSM_path2) as DSM_src:
    DSM2 = DSM_src.read(1)
    print("DSM2 shape", DSM2.shape, "DSM1 shape", DSM1.shape)

#viewing the raw drone flights
plt.imshow(DSM1, cmap='terrain', extent=rio.plot.plotting_extent(DSM_src))
plt.title('DSM1')
plt.show()  #uncomment to see the imagery

def padding(dsm1, dsm2):
    """
    This function takes 2 DSMs and pads them with 0's to make them the same shape. Returns the padded persion of the first input, 
    """
    max_rows = max(dsm1.shape[0], dsm2.shape[0])
    max_cols = max(dsm1.shape[1], dsm2.shape[1])
    DSM1_pad_rows = max_rows - dsm1.shape[0]
    DSM1_pad_cols = max_cols - dsm1.shape[1]
    #DSM2_pad_rows = max_rows - dsm2.shape[0]
    #DSM2_pad_cols = max_cols - dsm2.shape[1]

    padded1 = np.pad(dsm1, ((0, DSM1_pad_rows), (0, DSM1_pad_cols)), mode='constant', constant_values=0)
    return padded1

DSM1_padded = padding(DSM1, DSM2)
print("Now DSM2")
DSM2_padded = padding(DSM2, DSM1)
DIFF = DSM1_padded - DSM2_padded

diff_out_path = r"C:\GitHub\ALD_Drone_Processing\Outputs\differenced_odeheadridge.tiff"

with rio.open(
    diff_out_path,
    'w',
    driver='GTiff',
    width= DIFF.shape[1],
    height=DIFF.shape[0],
    count=1,
    dtype=DIFF.dtype,
    crs=DSM_src.crs,
    transform=DSM_src.transform,
) as diff_rast:
    diff_rast.write(DIFF, 1)

with rio.open(diff_out_path) as diff:
    DIFFERENCED = diff.read(1)

plt.imshow(DIFFERENCED, cmap='terrain', extent=rio.plot.plotting_extent(diff))
plt.title('Differenced DSM')
plt.show()  #uncomment to see the imagery