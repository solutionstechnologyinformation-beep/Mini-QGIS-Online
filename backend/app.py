from flask import Flask, request, jsonify
from flask_cors import CORS
from pyproj import Transformer

app = Flask(__name__)
CORS(app)

@app.route("/convert", methods=["POST"])
def convert():

    data = request.json

    x = float(data["x"])
    y = float(data["y"])
    src = data["src"]
    dst = data["dst"]

    transformer = Transformer.from_crs(
        f"EPSG:{src}",
        f"EPSG:{dst}",
        always_xy=True
    )

    new_x, new_y = transformer.transform(x, y)

    return jsonify({
        "x": new_x,
        "y": new_y
    })

if __name__ == "__main__":
    app.run(port=5000)