import serial
import configparser
import json

from time import sleep

# fix windows registry stuff
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import (
    Flask,
    Response,
    render_template,
    request
)
from flask_cors import CORS
from flask_socketio import SocketIO

# Read Configuration
config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__,
  static_url_path='/static',
  static_folder = "dist/static",
  template_folder = "dist"
)

app.config["SECRET_KEY"] = config["system"]["secret_key"]
app.config["DEBUG"] = config["system"]["debug"]

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app)

@app.errorhandler(404)
def not_found(e):
    return "Not Found", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return render_template("index.html")

# Update configfile values
@app.route("/interact_triggers", methods=["GET", "POST"])
def save_configfile():
    if request.method == "POST":
        data = {}

        with open('triggers.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        new_data = request.get_json(silent=True)
        triggers = new_data.get("triggers")
        idleTime = new_data.get("idleTime")

        data['triggers'] = triggers
        data['idleTime'] = idleTime

        with open('triggers.json', 'w') as f:
          json.dump(data, f)

        output = "Configuration Updated"
        return output
    elif request.method == "GET":
        f = open('triggers.json')
        output = json.load(f)
        f.close()

        return output

def read_serial_data():
    messageid = 0
    ser = serial.Serial()
    ser.port = config["serial"]["port"]
    ser.baudrate = config["serial"]["baudrate"]
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 0
    try:
        ser.open()
    except serial.SerialException as e:
         yield 'event:error\n' + 'data:' + 'Serial port error({0}): {1}\n\n'.format(e.errno, e.strerror)
         messageid = messageid + 1
    while True:
        data = ser.readline().decode('utf-8').strip()  # Read data from the serial port
        yield f'data: {data}\n\n'  # Yield data as Server-Sent Events (SSE)

@app.route('/serial_data')
def serial_data():
    solar_data = Response(read_serial_data(), mimetype='text/event-stream')
    solar_data.headers.add('Access-Control-Allow-Origin', '*')
    solar_data.headers.add('Cache-Control', 'no-cache')
    return solar_data

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=config["system"]["debug"])