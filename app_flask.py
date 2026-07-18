from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load model bundle
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_bundle.pkl")

bundle = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        bundle = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    if not bundle:
        return jsonify({'error': 'Model not found'}), 500
        
    try:
        data = request.get_json()
        
        # Expected features in order
        features = bundle['features']
        input_data = []
        for feature in features:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            input_data.append(data[feature])
            
        raw = np.array([input_data], dtype=float)
        
        # Transform
        transformer = bundle['transformer']
        transformed = transformer.transform(raw + 1e-6)
        
        # Predict
        model = bundle['model']
        strength = float(model.predict(transformed)[0])
        strength = max(0.0, strength)
        
        return jsonify({
            'prediction_mpa': strength,
            'features_used': features
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': bundle is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
