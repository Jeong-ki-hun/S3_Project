import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("hi.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    float_features = [(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    return render_template("hi.html", prediction_text = "너의 맘에드는 반팔티는! {}".format(prediction))

if __name__ == "__main__":
    flask_app.run(debug=True)