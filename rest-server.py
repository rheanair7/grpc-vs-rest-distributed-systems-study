#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response, jsonify
import jsonpickle
from PIL import Image
import base64
import io
import numpy as np
# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a,b):
    response = {'sum' : str( a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
    # build a response dict to send back to client
        response = {
            'width' : img.size[0],
            'height' : img.size[1]
            }
    except:
        response = { 'width' : 0, 'height' : 0}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    data = request.get_json()
    if 'a' not in data or 'b' not in data:
        return jsonify({'error': 'Missing a or b field'}), 400

    a = np.array(data['a'])
    b = np.array(data['b'])

    if len(a) != len(b):
        return jsonify({'error': 'Vectors must be same length'}), 400

    dot = float(np.dot(a, b))
    return jsonify({'dot': dot})

# route http posts to this method
@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        # Try parsing the JSON body
        data = request.get_json()
        print("Received JSON keys:", list(data.keys()) if data else None)

        if not data or 'image' not in data:
            print("❌ No 'image' field in JSON")
            return jsonify({'error': 'Missing image field'}), 400

        # Decode base64
        img_bytes = base64.b64decode(data['image'])
        print("✅ Image base64 decoded, length:", len(img_bytes))

        # Try opening with PIL
        image = Image.open(io.BytesIO(img_bytes))
        width, height = image.size
        print(f"✅ Image opened: width={width}, height={height}")

        return jsonify({'width': width, 'height': height})

    except Exception as e:
        print("🔥 Error in /api/jsonimage:", e)
        return jsonify({'error': str(e)}), 500


# start flask app
app.run(host="0.0.0.0", port=5000)