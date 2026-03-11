// Drawing tools with Turf.js for spatial analysis
var drawnItems = new L.FeatureGroup()
map.addLayer(drawnItems)

var drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems
    }
})

map.addControl(drawControl)

map.on(L.Draw.Event.CREATED, function (e) {
    var layer = e.layer
    drawnItems.addLayer(layer)
    
    // Analyze geometry with Turf.js
    if (layer.toGeoJSON) {
        var geoJSON = layer.toGeoJSON()
        analyzeFeature(geoJSON)
    }
})

function analyzeFeature(feature) {
    // Get area if polygon
    if (feature.geometry.type === 'Polygon') {
        var area = turf.area(feature)
        console.log('Area (m²):', area)
    }
    
    // Get length if line
    if (feature.geometry.type === 'LineString') {
        var distance = turf.length(feature, { units: 'kilometers' })
        console.log('Distance (km):', distance)
    }
}
