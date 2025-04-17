from io import BytesIO
import base64
from flask import Flask, render_template, request, jsonify
import qrcode
import validators

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    url = request.json.get('url', '').strip()
    if not validators.url(url):
        return jsonify({'error': 'URL tidak valid'}), 400
    
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    data = base64.b64encode(buf.getvalue()).decode('ascii')
    return jsonify({'img_data': f'data:image/png;base64,{data}', 'url': url})

if __name__ == '__main__':
    app.run(debug=True)