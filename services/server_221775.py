from flask import Flask, request
import tensorflow as tf

app = Flask(__name__)
classifier = tf.keras.applications.resnet.ResNet101()
with open("data/external/imagenet-labels.txt", "r") as f:
    classifier_labels = [i.rstrip().strip("\"") for i in f.readlines()]


@app.route("/")
def home_page():
    return "<h1>What's Crackin'?</h1>"


@app.post("/classify")
def classify():
    """Receive an image and return its predicted label."""
    data = request.data
    image = tf.io.decode_jpeg(data)
    image = tf.expand_dims(image, axis=0)
    image = tf.image.resize(image, (224, 224))
    output = classifier(image)
    indices = tf.argsort(output, direction="DESCENDING")[0, :3]
    output = [classifier_labels[int(i)] for i in indices]
    return output
