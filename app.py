from flask import Flask, render_template, request, jsonify
from joblib import load


loaded_model, loaded_vectorizer = load("SVC_models.joblib")

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        news_text = request.form.get('news_content') or request.json.get('news_content')
        
        if not news_text:
            return jsonify({'error': 'No news content provided'}), 400

        
        transformed_text = loaded_vectorizer.transform([news_text])

        
        prediction = loaded_model.predict(transformed_text)[0]

        
        result = "REAL" if prediction == 1 else "FAKE"
        return jsonify({'prediction': result})

    return jsonify({'error': 'Invalid request method'}), 405

if __name__ == "__main__":
    app.run(debug=True)