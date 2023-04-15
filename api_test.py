import requests

url = "http://127.0.0.1:5000/detections"
image_path = "/home/tanish/Desktop/Dev/ML/API/yolov3-tf2/data/download.jpeg"

with open(image_path, "rb") as f:
    response = requests.get(url)
    print(response.text)