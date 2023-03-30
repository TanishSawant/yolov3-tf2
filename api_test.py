import requests

url = "http://b29d-2404-bd00-3-d7f7-ffbf-294-ffe0-9ab5.ngrok.io/image"
image_path = "/home/tanish/Desktop/Dev/ML/API/yolov3-tf2/detections/detection.jpg"

with open(image_path, "rb") as f:
    response = requests.post(url, files={"images": f})
    print(response.text)