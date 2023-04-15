import time
from absl import app, logging
import cv2
import numpy as np
import tensorflow as tf
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from flask import jsonify
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs
from flask import Flask, request, Response, jsonify, send_from_directory, abort
import os
from flask_ngrok import run_with_ngrok

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary
import requests
import urllib
from PIL import Image
import numpy as np
import pyimgur

imgur_client_id = '2eadeec4f0227cf'
imgur_client = pyimgur.Imgur(imgur_client_id)



cloudinary.config(
  cloud_name = "dgyqb1z2g",
  api_key = "545892885457815",
  api_secret = "dc4jz6zhdoTsN97FFsYw6FR5qfc",
  secure = True
)

# # customize your API through the following parameters
classes_path = './data/strawberry.names'
weights_path = '/home/tanish/Desktop/Dev/ML/yolov3-tf2/checkpoints/yolov3_train_20.tf'
tiny = False                    # set to True if using a Yolov3 Tiny model
size = 416                      # size images are resized to for model
output_path = './detections/'   # path to output folder where images with detections are saved
num_classes = 2             # number of classes in model

# # load in weights and classes
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

if tiny:
    yolo = YoloV3Tiny(classes=num_classes)
else:
    yolo = YoloV3(classes=num_classes)

yolo.load_weights(weights_path).expect_partial()
print('weights loaded')

class_names = [c.strip() for c in open(classes_path).readlines()]
print('classes loaded')

# Initialize Flask application
app = Flask(__name__)
# run_with_ngrok(app)
# API that returns JSON with classes found in images
@app.route('/detections', methods=['GET'])
def get_detections():

    #call Neel
    url = "http://127.0.0.1:8081/"


    response_url = requests.post(url, json={"service":"camera"}) #considering response is the url
    print(response_url.text)
    urllib.request.urlretrieve(response_url.text, 'image.jpg')
    #
    raw_images = []

    img_raw = tf.image.decode_image(open('image.jpg', 'rb').read(), channels=3)
    raw_images.append(img_raw)
    image_names = ['image.jpg',]

    #images = request.files.getlist("images")
    
    # for image in images:
    #     image_name = image.filename
    #     image_names.append(image_name)
    #     image.save(os.path.join(os.getcwd(), image_name))
    #     img_raw = tf.image.decode_image(
    #         open(image_name, 'rb').read(), channels=3)
    #     raw_images.append(img_raw)
    num = 0
    
    # create list for final response
    response = []

    for j in range(len(raw_images)):
        # create list of responses for current image
        responses = []
        raw_img = raw_images[j]
        num+=1
        img = tf.expand_dims(raw_img, 0)
        img = transform_images(img, size)

        t1 = time.time()
        boxes, scores, classes, nums = yolo(img)
        t2 = time.time()
        print('time: {}'.format(t2 - t1))

        print('detections:')
        for i in range(nums[0]):
            # print('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
            #                                 np.array(scores[0][i]),
            #                                 np.array(boxes[0][i])))
            responses.append([
                class_names[int(classes[0][i])], float("{0:.2f}".format(np.array(scores[0][i])*100))
            ])

        # print(responses)
        response = responses
        img = cv2.cvtColor(raw_img.numpy(), cv2.COLOR_RGB2BGR)
        img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
        cv2.imwrite(output_path + 'detection' + str(num) + '.jpg', img)
        print('output saved to: {}'.format(output_path + 'detection' + str(num) + '.jpg'))
    print("Shit")
    #remove temporary images
    for name in image_names:
        os.remove(name)
    print("=============================")
    print(responses)
    try:

        return jsonify(response), 200
    except FileNotFoundError:
        abort(404)


@app.route("/", methods=["GET"])
def gello():
    return({"mst":"wfu"})

# API that returns image with detections on it
@app.route('/image', methods= ['GET'])
def get_image():

    #call Neel
    # url = "https://056d-42-106-240-194.in.ngrok.io/"
    url = 'http://localhost:8081/'
    response = requests.post(url, json={"service":"camera"}) #considering response is the url
    urllib.request.urlretrieve(response.text, 'image.jpg')
    #
    image_name = 'image.jpg'
    # image = request.files["images"]
    # image_name = image.filename
    # image.save(os.path.join(os.getcwd(), image_name))
    img_raw = tf.image.decode_image(
        open(image_name, 'rb').read(), channels=3)
    img = tf.expand_dims(img_raw, 0)
    img = transform_images(img, size)

    t1 = time.time()
    boxes, scores, classes, nums = yolo(img)
    t2 = time.time()
    print('time: {}'.format(t2 - t1))

    print('detections:')
    for i in range(nums[0]):
        print('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                        np.array(scores[0][i]),
                                        np.array(boxes[0][i])))
    img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
    img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
    cv2.imwrite(output_path + 'detection.jpg', img)
    print('output saved to: {}'.format(output_path + 'detection.jpg'))
    # upload(output_path + 'detection.jpg', public_id="image", overwrite=True)
    # url, options = cloudinary_url("image", crop="fill")
    # image_path = output_path + "detection.jpg"
    # print(url)
    uploaded_image = imgur_client.upload_image(output_path + 'detection.jpg') 
    print(uploaded_image.link)
    img_url = uploaded_image.link
    
    # prepare image for response
    # _, img_encoded = cv2.imencode('.png', img)
    # response = img_encoded.tobytes()
    
    #remove temporary image
    os.remove(image_name)

    try:
        return jsonify({"response" : img_url}), 200
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(debug = True)