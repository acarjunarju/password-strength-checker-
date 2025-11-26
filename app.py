import re
import random
import string
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# IMPORTANT: explicitly set the template folder
app = Flask(__name__, template_folder='templates')
CORS(app)

# --- THIS IS THE MISSING PART ---
# This tells Flask: "When someone visits the home page, show them index.html"
@app.route('/')
def home():
    return render_template('index.html')

# --- Existing Logic Below ---

def check_password_strength(password):
    score = 0
    feedback = []
    
    length = len(password)
    if length < 8:
        feedback.append("Password is too short (min 8 chars).")
    elif length >= 12:
        score += 2
        feedback.append("Good length.")
    else:
        score += 1
        feedback.append("Acceptable length.")

    if re.search(r"[a-z]", password): score += 1
    else: feedback.append("Add lowercase letters.")
        
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("Add uppercase letters.")
        
    if re.search(r"\d", password): score += 1
    else: feedback.append("Add numbers.")
        
    if re.search(r"[ !#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", password): score += 1
    else: feedback.append("Add special characters (@, #, $, etc).")

    if length < 8:
        final_score = 10
        strength_label = "Very Weak"
    else:
        raw_score = score
        if raw_score <= 2:
            final_score = 25
            strength_label = "Weak"
        elif raw_score == 3:
            final_score = 50
            strength_label = "Moderate"
        elif raw_score == 4:
            final_score = 75
            strength_label = "Strong"
        else:
            final_score = 100
            strength_label = "Very Strong"

    return {
        "score": final_score,
        "label": strength_label,
        "feedback": feedback
    }

@app.route('/api/check', methods=['POST'])
def api_check_strength():
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({"error": "No password provided"}), 400
    password = data['password']
    result = check_password_strength(password)
    return jsonify(result)

@app.route('/api/generate', methods=['GET'])
def api_generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choice(chars) for i in range(16))
    return jsonify({"password": password})

if __name__ == '__main__':
    # Use 0.0.0.0 for Render to be able to detect the port
    app.run(host='0.0.0.0', port=5000)
