import serial
import configparser
import json
import threading
import time
import random

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

from modules.utility import check_json_file, tasmota_setStatus

# Read Configuration
config = configparser.ConfigParser()
config.read("config.ini")

data = check_json_file('triggers.json')
# Prefill timers
for trigger in data['triggers']:
    trigger['start_time'] = time.time()
    trigger['triggered'] = 'off'

# Start App definition
app = Flask(__name__,
  static_url_path='/static',
  static_folder = "dist/static",
  template_folder = "dist"
)

app.config["SECRET_KEY"] = config["system"]["secret_key"]
app.config["DEBUG"] = config["system"]["debug"]

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, always_connect=True, async_mode='threading')

def socketio_server():
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)

def background_function():
    while True:
        x = random.randint(9, 20) # Random value test
        print('x', x)

        for trigger in data['triggers']:
            if x > int(trigger['value']):
                elapsed_time = time.time() - trigger['start_time']
                if elapsed_time >= data['triggerTime']:  # in seconds
                    trigger['triggered'] = 'on'
                    tasmota_setStatus(trigger['device'], trigger['triggered'])
            else:
                trigger['start_time'] = time.time()  # Reset start time if value drops below x
                if trigger['triggered'] == 'on':
                    trigger['triggered'] = 'off'
                    tasmota_setStatus(trigger['device'], trigger['triggered'])

        print(data['triggers'])
        time.sleep(data['idleTime'])  # Sleep for idleTime seconds before running again

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
        triggerTime = new_data.get("triggerTime")

        data['triggers'] = triggers
        data['idleTime'] = idleTime
        data['triggerTime'] = triggerTime

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
    try:
        # Start the Flask app in a separate thread
        socketio_thread = threading.Thread(target=socketio_server)
        socketio_thread.daemon = True
        socketio_thread.start()
        
        # Start the background function in the main thread
        background_function()
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught. Exiting...")