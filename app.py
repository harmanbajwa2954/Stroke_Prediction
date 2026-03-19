from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Load the model and columns using pickle
with open('stroke_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('stroke_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Receive JSON data from the client
        data = request.get_json()
        df = pd.DataFrame([data])

        # 2. Preprocess: One-hot encode the incoming data
        df_encoded = pd.get_dummies(df)

        # 3. Align columns (Fills missing one-hot columns with 0 to match training data)
        df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)

        # 4. Make Prediction
        prediction = model.predict(df_encoded)[0]
        probability = model.predict_proba(df_encoded)[0][1]

        # 5. Return JSON response
        return jsonify({
            'stroke_prediction': int(prediction),
            'stroke_probability': round(float(probability), 4),
            'risk_level': 'High Risk' if prediction == 1 else 'Low Risk'
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the app locally on port 5000
    app.run(debug=True, host='0.0.0.0', port=7860)
