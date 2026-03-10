from pyproj import Transformer

def convert(x,y,src,dst):

    transformer = Transformer.from_crs(
        f"EPSG:{src}",
        f"EPSG:{dst}",
        always_xy=True
    )

    return transformer.transform(x,y)