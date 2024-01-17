import pickle
from flask import Flask, request

app = Flask(__name__)

with open("employee churn/churn_model.pkl", "rb") as file:
    model = pickle.load(file)

@app.route("/")
def home_page():
    return f"Welcome, Hello World!!!"

@app.route("/sample-data", methods = ["GET"])
def sample_data():
    sample_data_format = {"name" : "Praveen Allam"}
    return f"sample data : {sample_data_format}"

@app.route("/predict", methods = ["POST", "GET"])
def predict():
    return "prediction being done"
