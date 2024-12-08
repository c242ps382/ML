from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import pickle

app = Flask(__name__)

# Load model
interpreter = tf.lite.Interpreter(model_path='disease_model.tflite')
interpreter.allocate_tensors()
# Input dan output dari model tflite
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load label encoder
with open('label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)

# Load features/symptoms
with open('features.pkl', 'rb') as file:
    symptoms = pickle.load(file)

# Load mapping of disease to code
with open('disease_code_map.pkl', 'rb') as file:
    disease_code_map = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    if not request.json or 'symptoms' not in request.json:
        return jsonify({'error': 'Invalid request, JSON with "symptoms" key is required'}), 400

    # Dapatkan input gejala dari JSON
    selected_symptoms = request.json['symptoms']  # List of symptoms
    input_data = np.zeros(len(symptoms))
    
    for symptom in selected_symptoms:
        if symptom in symptoms:
            idx = symptoms.index(symptom)
            input_data[idx] = 1

    input_data = input_data.reshape(1, -1).astype(np.float32)

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # Run inference
    interpreter.invoke()
    # Hasil predict
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    # Top 3 predict
    top_3_idx = predictions.argsort()[-3:][::-1]
    prediction_results = []

    for idx in top_3_idx:
        disease = label_encoder.inverse_transform([idx])[0]
        probability = predictions[idx] * 100
        code = disease_code_map.get(disease, "N/A")
        prediction_results.append({
            'disease': disease,
            'code': code,
            'probability': probability
        })

    return jsonify({'predictions': prediction_results})

if __name__ == '__main__':
    app.run(debug=True)
