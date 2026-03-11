// Initialize map and add base layers with Turf.js integration
var map = L.map('map').setView([-23.5505, -46.6333], 10)

var satellite = L.tileLayer(
'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
{
maxZoom:19
})

var osm = L.tileLayer(
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{
maxZoom:19
})

var baseMaps = {
"OpenStreetMap": osm,
"Satellite": satellite
}

osm.addTo(map)
L.control.layers(baseMaps).addTo(map)

// Turf.js utility functions
function getDistance(point1, point2) {
    var from = turf.point(point1)
    var to = turf.point(point2)
    return turf.distance(from, to, { units: 'kilometers' })
}

function getBoundingBox(coordinates) {
    var points = coordinates.map(coord => turf.point(coord))
    var featureCollection = turf.featureCollection(points)
    return turf.bbox(featureCollection)
}