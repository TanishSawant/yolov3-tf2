from flask import Flask
import os
import re
import operator
import requests
import json
import base64
from flask import request
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)



@app.route('/',  methods=['POST'])
def workflow():
    req = json.loads(request.data)
    val = req["service"]
    print(val)
    if val == "camera":  
        return "https://i.imgur.com/lT14jJC.jpg"

    if val == "footage":
        return "https://i.imgur.com/lT14jJC.jpg"

    if val == "forward":
        return "Moved Forward"

    if val == "right":
        return "Moved Right"

    if val == "left":
        return "Moved Left"

    if val == "backward":
        return "Moved Backward"

    if val == "motor1":
        direction = req["direction"]
        if direction == "upward":
            #motor1_forward()
            return "Motor1 - Upward"
        elif direction == "downward":
            #motor1_reverse()
            return "Motor1 - Downward"
        else:
            #motor1_stop()
            return "Motor1 - Stop"

    if val == "motor2":
        direction = req["direction"]
        if direction == "backward":
            #motor2_forward()
            return "Motor2 - Backward"
        elif direction == "forward":
            #motor2_reverse()
            return "Motor2 - Forward"
        else:
            #motor2_stop()
            return "Motor2 - Stop"
    print("Nothing specified")
    return "None"

if __name__ == "__main__":
    app.run(port=8081)