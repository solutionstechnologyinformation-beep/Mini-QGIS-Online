var map = L.map('map').setView([-15,-55],4);

L.tileLayer(
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{
maxZoom:19
}
).addTo(map);

map.on("click", function(e){

document.getElementById("x").value = e.latlng.lng
document.getElementById("y").value = e.latlng.lat

});