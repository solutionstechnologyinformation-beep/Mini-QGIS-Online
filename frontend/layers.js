// Layer management with Turf.js spatial analysis
var layers = {}

function addLayer(name, geoJSON) {
    var geoJSONLayer = L.geoJSON(geoJSON, {
        onEachFeature: function (feature, layer) {
            layer.bindPopup(JSON.stringify(feature.properties))
        }
    })
    
    geoJSONLayer.addTo(map)
    layers[name] = geoJSONLayer
    
    return geoJSONLayer
}

function removeLayer(name) {
    if (layers[name]) {
        map.removeLayer(layers[name])
        delete layers[name]
    }
}

function getLayerBounds(name) {
    if (layers[name]) {
        return layers[name].getBounds()
    }
}

function bufferLayer(name, distance, units = 'kilometers') {
    if (layers[name]) {
        var geoJSONData = layers[name].toGeoJSON()
        var buffered = turf.buffer(geoJSONData, distance, { units: units })
        return addLayer(name + '_buffer', buffered)
    }
}

function intersectLayers(name1, name2) {
    if (layers[name1] && layers[name2]) {
        var geoJSON1 = layers[name1].toGeoJSON()
        var geoJSON2 = layers[name2].toGeoJSON()
        
        var intersection = turf.intersect(geoJSON1, geoJSON2)
        return intersection
    }
}
