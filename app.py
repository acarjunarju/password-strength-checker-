import re
import random
import string
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so the HTML file can communicate with this server from a browser
CORS(app)

def check_password_strength(password):
    """
    Analyzes password strength based on length and character variety.
    Returns a dictionary with score, message, and specific feedback.
    """
    score = 0
    feedback = []
    
    # 1. Length Check
    length = len(password)
    if length < 8:
        feedback.append("Password is too short (min 8 chars).")
    elif length >= 12:
        score += 2
        feedback.append("Good length.")
    else:
        score += 1
        feedback.append("Acceptable length.")

    # 2. Complexity Checks
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")
        
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")
        
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")
        
    if re.search(r"[ !#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", password):
        score += 1
    else:
        feedback.append("Add special characters (@, #, $, etc).")

    # Normalize Score (0 to 100 scale for UI)
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
    """Generates a strong random password."""
    # Define the character set: Uppercase, Lowercase, Digits, and Punctuation
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    
    # Generate a random 16-character password
    password = "".join(random.choice(chars) for i in range(16))
    
    return jsonify({"password": password})

if __name__ == '__main__':
    print("Starting Flask Server on Port 5000...")
    app.run(debug=True, port=5000)