var ibge = L.tileLayer.wms(
"http://localhost:8080/geoserver/ibge/wms",
{
layers:"ibge:municipios",
transparent:true
}
)

ibge.addTo(map)
var mapbiomas = L.tileLayer.wms(
"http://localhost:8080/geoserver/mapbiomas/wms",
{
layers:"mapbiomas:cobertura",
transparent:true
}
)
mapbiomas.addTo(map)