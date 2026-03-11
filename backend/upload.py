"""File upload handling and processing for spatial data."""
import geopandas as gpd
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../data/uploads'
ALLOWED_EXTENSIONS = {'shp', 'geojson', 'json', 'gpkg', 'kml'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_shapefile(path):
    """Read shapefile and return as GeoJSON."""
    try:
        gdf = gpd.read_file(path)
        return gdf.to_json()
    except Exception as e:
        return {'error': str(e)}

def read_geojson(path):
    """Read GeoJSON file."""
    try:
        gdf = gpd.read_file(path)
        return gdf.to_json()
    except Exception as e:
        return {'error': str(e)}

def process_upload(file):
    """Process uploaded file and return GeoJSON."""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)
        
        if filename.endswith('.shp'):
            return read_shapefile(filepath)
        else:
            return read_geojson(filepath)
    
    return {'error': 'Invalid file type'}
