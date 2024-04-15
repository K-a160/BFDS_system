# from flask import Flask, request, jsonify, render_template
# import numpy as np
# import joblib
# app = Flask(__name__)

# # Load the trained model
# model = joblib.load("fraud_detection_ model_mine.pkl")

# @app.route('/')
# def home():
#     return render_template('index.html')



# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get data from request
#     data = request.get_json(force=True)
#     # Convert data to numpy array
#     features = np.array(data['features']).reshape(1, -1)
#     # Make prediction
#     prediction = model.predict(features)[0]
#     # Return prediction result
#     return jsonify({'prediction': 'Fraud' if prediction == 'Fraud' else 'No Fraud'})
# if __name__ == '__main__':
#     app.run(debug=False)



from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import sqlite3

app = Flask(__name__)

# Load the trained model
model = joblib.load("fraud_detection_model_mine.pkl")

# Function to create SQLite connection and cursor
def get_db():
    conn = sqlite3.connect('fraud_detection.db')
    cursor = conn.cursor()
    return conn, cursor

# Function to create table if not exists
def create_table():
    conn, cursor = get_db()
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions 
                      (username TEXT, email TEXT, type INTEGER, amount REAL, oldbalanceOrg REAL, newbalanceOrig REAL, prediction TEXT)''')
    conn.commit()
    conn.close()

# Create table on startup
create_table()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from request
    data = request.get_json(force=True)
    print(data)
    email = data.get('email')
    username = data.get('username')
    features = data.get('features')
    type_ = features[0]
    amount = features[1]
    oldbalanceOrg = features[2]
    newbalanceOrig = features[3]

    
    print("Extracted values:", username, email, type_, amount, oldbalanceOrg, newbalanceOrig)

    # Make predictionr
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)[0]
    
    # Store data and prediction in database
    conn, cursor = get_db()
    cursor.execute("INSERT INTO predictions (username, email, type, amount, oldbalanceOrg, newbalanceOrig, prediction) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (username, email, type_, amount, oldbalanceOrg, newbalanceOrig, prediction))
    conn.commit()
    conn.close()
    
    # Return prediction result
    return jsonify({'prediction': 'Fraud' if prediction == 'Fraud' else 'No Fraud'})

if __name__ == '__main__':
    app.run(debug=False)









