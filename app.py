from flask import Flask, request, send_file, render_template
from PIL import Image
from io import BytesIO
from zipfile import ZipFile

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')
    if not images:
        return ('No files uploaded', 400)

    converted = []
    for image in images:
        img = Image.open(image)
        buf = BytesIO()
        img.save(buf, format='WEBP')
        buf.seek(0)
        base = image.filename.rsplit('.', 1)[0] if image.filename else 'image'
        converted.append((f'{base}.webp', buf))

    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zf:
        for filename, buffer in converted:
            zf.writestr(filename, buffer.read())
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name='converted_images.zip', mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=True)
