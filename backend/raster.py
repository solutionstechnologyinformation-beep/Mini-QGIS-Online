import rasterio

def info(file):

    with rasterio.open(file) as src:

        return {
            "width":src.width,
            "height":src.height,
            "crs":str(src.crs)
        }