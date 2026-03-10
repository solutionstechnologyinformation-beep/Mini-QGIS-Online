from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)