import json
import os
import requests

# Check for file
def check_json_file(filename):
    if os.path.exists(filename):
        print(f"File '{filename}' exists.")
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    else:
        print(f"File '{filename}' does not exist. Creating empty JSON file.")
        with open(filename, 'w') as file:
            json.dump({}, file)
        return {}
    
def tasmota_setStatus(device, status):
    if status == 'on' or status == 'off':
        try:
            r = requests.get("http://{ip}/cm?cmnd=Power%20{status}".format(ip=device, status=status.capitalize() )).content
            return r
        except requests.exceptions.Timeout:
            return print('Timeout while trying to contact Tasmota device')
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            return print('TooManyRedirects')
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.ConnectionError:
            return print('ConnectionError')
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)
    else:
        print('Please use only on or off')