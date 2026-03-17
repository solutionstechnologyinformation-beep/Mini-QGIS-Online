from flask import Flask, jsonify
from backend.spatial import convert

app = Flask(__name__)

@app.route("/convert/<x>/<y>")
def convert_coord(x,y):

    nx,ny = convert(
        float(x),
        float(y),
        "EPSG:4326",
        "EPSG:31983"
    )

    return jsonify({
        "x":nx,
        "y":ny
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)