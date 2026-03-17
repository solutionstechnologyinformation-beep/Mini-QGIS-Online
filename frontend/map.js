var map = L.map('map').setView([-14,-52],4)

var osm = L.tileLayer(
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{
maxZoom:19
})

osm.addTo(map)