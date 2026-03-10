async function convert(){

let x = document.getElementById("x").value
let y = document.getElementById("y").value
let src = document.getElementById("src").value
let dst = document.getElementById("dst").value

let response = await fetch("http://localhost:5000/convert",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
x:x,
y:y,
src:src,
dst:dst
})

})

let data = await response.json()

document.getElementById("result").innerText =
data.x + " , " + data.y

}