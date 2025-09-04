from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from scipy.stats import mode
from consultation import medical_consultation, mental_consultation,predicted_consultation
import pickle

app = Flask(__name__, static_folder='assets', static_url_path='/assets')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/general.html', methods=['GET', 'POST'])
def general():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        query = request.form['query']
        
        response = medical_consultation(age, gender, query)
        return jsonify({'response': response})
    
    return render_template('general.html')


@app.route('/mental.html', methods=['GET', 'POST'])
def mental():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        stress_level = request.form['stressLevel']
        sleep_quality = request.form['sleepQuality']
        mood = request.form['mood']
        concern = request.form['concern']
        
        response = mental_consultation(age, gender, stress_level, sleep_quality, mood, concern)
        return jsonify({'response': response})
    
    return render_template('mental.html')


@app.route('/prediction.html' , methods=['GET','POST'])
def prediction():
    if request.method=='POST':
        data = request.get_json()
        symptoms = data.get('symptoms', [])

        prediction = predict_disease(symptoms)  # your diseease_prediction.py logic
        return jsonify({'response': prediction })
    return render_template('prediction.html')

@app.route('/pred' , methods=['GET','POST'])
def pred():
    if request.method=='POST':
        data = request.get_json()
        disease = data.get('disease')
        prediction = predicted_consultation(disease)  
        return jsonify({'response': prediction })

# Load models and label encode
random_forest_model = joblib.load('models/random_forest_model.pkl')
naive_bayes_model = joblib.load('models/naive_bayes_model.pkl')
decision_tree_model = joblib.load('models/decision_tree_model.pkl')
le = joblib.load('models/label_encoder.pkl')
all_symptoms = joblib.load('models/all_symptoms_list.pkl')


def predict_disease(chosen_symptoms):
    input_vector = [1 if symptom in chosen_symptoms else 0 for symptom in all_symptoms]
    print(input_vector)
    rf_pred = random_forest_model.predict([input_vector])
    nb_pred = naive_bayes_model.predict([input_vector])
    dt_pred = decision_tree_model.predict([input_vector])
    
    predictions = np.array([rf_pred, nb_pred, dt_pred])
    majority_vote = mode(predictions, axis=0)[0].flatten()
    
    final_disease = le.inverse_transform(majority_vote)
    return final_disease[0]
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
