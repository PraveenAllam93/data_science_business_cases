import pickle
from flask import Flask, request,jsonify
import numpy as np
import pandas as pd
import json

app = Flask(__name__)

with open("employee churn/churn_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("employee churn/encoder.pkl", "rb") as file:
    encoder = pickle.load(file)

@app.route("/")
def home_page():
    return f"Welcome, Hello World!!!"

@app.route("/sample-data", methods = ["GET"])
def sample_data():
    sample_data_format =    {
                                "Income_last" : "current month income",
                                "Income_mean" : "Average of your total income",
                                "City_last" : "current city you're working",
                                "Total Business Value_sum"	: "total business value",
                                "Total Business Value_min" : "minimum business value",
                                "Total Business Value_max" : "maximum business value",	
                                "Total Business Value_mean" : "mean business value",	
                                "Total Business Value_last" : "last business value",	
                                "Education_Level_last" : "current education level",	
                                "Joining Designation_last" : "current joining designation",	
                                "Age_max" : "cuurent age",	
                                "Grade_min" : "minimum grade",	
                                "Grade_max" : "maximum grade",	
                                "Grade_mean" : "average grade",	
                                "Grade_last" : "last grade",	
                                "Quarterly Rating_max" : "maximum quaterly rating",	
                                "Gender_last" : "gender",	
                                "rating_change" : "any change in quaterly rating (increased or not)",	
                                "income_change" : "any change in income (increased or not)",
                                "days_worked" : "number of days worked",	
                                "current_month" : "present month"
                            }
    return jsonify(sample_data_format)

@app.route("/predict", methods=["POST", "GET"])
def predict():

    employee_details = request.get_json()

    # Convert gender to numerical value (assuming 'male' = 0 and 'female' = 1)
    # gender_mapping = {'male': 0, 'female': 1}
    # employee_details["Gender_last"] = gender_mapping.get(employee_details["Gender_last"], 1)  # Default to female if not specified

    if 'City_last' in employee_details and len(employee_details['City_last']) > 0:
        employee_details['City_last'] = employee_details['City_last'][1:]


    data = pd.Series(employee_details)
    data = pd.DataFrame(data.values.reshape(1, data.shape[0]), columns = employee_details.keys())


    columns_order = ['Income_mean', 'Income_last', 'Total Business Value_sum',
       'Total Business Value_min', 'Total Business Value_max',
       'Total Business Value_mean', 'Total Business Value_last', 'City_last',
       'Education_Level_last', 'Joining Designation_last', 'Age_max',
       'Grade_min', 'Grade_max', 'Grade_mean', 'Grade_last',
       'Quarterly Rating_max', 'Gender_last', 'rating_change', 'income_change',
       'days_worked', 'current_month']
    data = data[columns_order]

    int_data = ["City_last", "rating_change", "income_change", "current_month"] 
    for col in data.columns:
        if col in int_data:
            data[col] = data[col].astype("int64")
        else:    
            data[col] = data[col].astype("float64")

    # Encode the data
    data_encoded = encoder.transform(data)


    churn_status = model.predict(data_encoded)

    churn_status_list = churn_status.tolist()  # Convert ndarray to list
    response_data = {'status': 200, 'churn_status': churn_status_list}  # Create a dictionary to be returned
    return json.dumps(response_data)

if __name__ == '__main__':
    app.run(debug=True)

