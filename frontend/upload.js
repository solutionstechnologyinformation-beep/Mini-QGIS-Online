document.getElementById("file").addEventListener("change", function(e){

var file = e.target.files[0]

var reader = new FileReader()

reader.onload = function(evt){

var geojson = JSON.parse(evt.target.result)

L.geoJSON(geojson).addTo(map)

}

reader.readAsText(file)

})