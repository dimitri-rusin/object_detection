import flask
import glob
import os
import ssl
import ultralytics

app = flask.Flask(__name__)

@app.route('/yolo', methods=['GET', 'POST'])
def get_traces_handle():
  try:

    with open('bus_received.jpg', 'wb') as binary_image:
      binary_image.write(flask.request.data)

    model = ultralytics.YOLO("yolov8n.pt")
    # runs/detect/predict0043/bus_received.jpg
    results = model.predict(
      source='bus_received.jpg',
      save=True,
    )

    # At this point we assume, since no exception has been raised by model.predict(),
    # that the function was successful and the desired file is the most recently
    # modified regular file in the current directory.
    print(results)

    # Get all files in the current directory
    files = glob.glob('./runs/**/*', recursive=True)

    # Find the most recently modified file
    latest_file = max(files, key=os.path.getmtime)

    print(latest_file)

    # Open the file in binary mode and read it
    with open(latest_file, 'rb') as f:
        file_bytes = f.read()

    # Create a response with the file bytes
    flask_response = flask.make_response(file_bytes)

    # Set the appropriate content type
    flask_response.headers.set('Content-Type', 'image/jpeg')

    # Optionally, set the content disposition to allow for file download
    flask_response.headers.set('Content-Disposition', 'attachment', filename='filename.jpg')

    return flask_response
  except Exception as exception:
    flask_response = flask.make_response(str(exception))
    flask_response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    print(flask_response)
    return flask_response

@app.after_request
def add_cors_headers(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  return response

if __name__ == '__main__':
  # Enable HTTPS using self-signed certificates
  context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
  context.load_cert_chain('certificate.pem', 'key.pem')

  app.run(
    host='0.0.0.0',
    port=8080,
    debug=True,
    use_reloader=False,
    ssl_context=context,
  )
