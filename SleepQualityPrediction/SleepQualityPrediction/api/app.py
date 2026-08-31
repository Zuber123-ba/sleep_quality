from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import pickle
import os
from functools import wraps

# ✅ Correct package imports
from face_analysis import analyze_face, analyze_face_image
from predictor import sleep_need_from_face
from recommendation import get_recommendations
from report_generator import generate_pdf
from auth import register_user, login_user, verify_token, logout_user, get_user_profile
from profession_questionnaire import get_profession_questions, analyze_sleep_responses

# ---------------------------------------------------
# APP CONFIG
# ---------------------------------------------------
app = Flask(__name__, static_folder="../frontend")
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

os.makedirs(REPORT_DIR, exist_ok=True)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------
model_path = os.path.join(MODEL_DIR, "sleep_model.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError("❌ sleep_model.pkl not found")

with open(model_path, "rb") as f:
    model = pickle.load(f)

LABELS = {0: "Bad", 1: "Good", 2: "Best"}

# ---------------------------------------------------
# 🔐 AUTHENTICATION DECORATOR
# ---------------------------------------------------
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]  # Remove 'Bearer ' prefix
        
        if not token:
            return jsonify({"error": "Authentication required"}), 401
        
        auth_result = verify_token(token)
        if not auth_result['valid']:
            return jsonify({"error": auth_result['error']}), 401
        
        # Add user info to request context
        request.current_user = auth_result['user']
        return f(*args, **kwargs)
    
    return decorated_function

# ---------------------------------------------------
# 🔐 AUTHENTICATION ROUTES
# ---------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        result = register_user(data)
        
        if result['success']:
            return jsonify({"message": result['message']}), 201
        else:
            return jsonify({"error": result['error']}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        result = login_user(email, password)
        
        if result['success']:
            return jsonify({
                "token": result['token'],
                "user": result['user']
            }), 200
        else:
            return jsonify({"error": result['error']}), 401
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logout", methods=["POST"])
def logout():
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
        
        if not token:
            return jsonify({"error": "Token required"}), 400
        
        result = logout_user(token)
        
        if result['success']:
            return jsonify({"message": result['message']}), 200
        else:
            return jsonify({"error": result['error']}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/profile", methods=["GET"])
@require_auth
def profile():
    try:
        return jsonify({"user": request.current_user}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verify-token", methods=["POST"])
def verify_user_token():
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
        
        if not token:
            return jsonify({"valid": False, "error": "Token required"}), 400
        
        result = verify_token(token)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500

# ---------------------------------------------------
# 📝 PROFESSION-BASED QUESTIONNAIRE ROUTES
# ---------------------------------------------------
@app.route("/questionnaire/questions", methods=["GET"])
@require_auth
def get_questionnaire_questions():
    try:
        user = request.current_user
        profession = user.get('profession', 'other')
        
        questions_data = get_profession_questions(profession)
        return jsonify(questions_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/questionnaire/submit", methods=["POST"])
@require_auth
def submit_questionnaire():
    try:
        user = request.current_user
        profession = user.get('profession', 'other')
        
        responses = request.get_json()
        if not responses:
            return jsonify({"error": "No responses provided"}), 400
        
        # Analyze responses and generate results
        analysis = analyze_sleep_responses(responses, profession)
        
        # Add user info to analysis
        analysis['user_info'] = {
            'name': user['name'],
            'profession': profession,
            'age': user['age']
        }
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------
# 🏠 SERVE FRONTEND (VERY IMPORTANT)
# ---------------------------------------------------
@app.route("/")
def welcome():
    return send_from_directory(FRONTEND_DIR, "welcome.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/user-profile")
def user_profile_page():
    return send_from_directory(FRONTEND_DIR, "profile.html")

@app.route("/sleep-assessment")
def sleep_assessment_page():
    return send_from_directory(FRONTEND_DIR, "profession-questionnaire.html")

@app.route("/<path:path>")
def frontend_files(path):
    return send_from_directory(FRONTEND_DIR, path)

# ---------------------------------------------------
# 1️⃣ ML PREDICTION (JSON)
# ---------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame([data])

        pred = model.predict(df)[0]
        label = LABELS.get(pred, "Unknown")

        recommendations = get_recommendations(data, label)
        pdf_file = generate_pdf(data, label, recommendations)

        return jsonify({
            "label": label,
            "recommendations": recommendations,
            "report": pdf_file
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------
# 2️⃣ CSV PREDICTION (FIXED FOR FETCH)
# ---------------------------------------------------
@app.route("/predict_csv", methods=["POST"])
def predict_csv():
    if "file" not in request.files:
        return jsonify({"error": "No CSV uploaded"}), 400

    try:
        file = request.files["file"]
        df = pd.read_csv(file)

        preds = model.predict(df)
        df["prediction"] = preds
        df["label"] = df["prediction"].map(LABELS)

        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------
# 3️⃣ DOWNLOAD PDF
# ---------------------------------------------------
@app.route("/download/<filename>")
def download_report(filename):
    return send_from_directory(REPORT_DIR, filename, as_attachment=True)

# ---------------------------------------------------
# 4️⃣ FACE + EYE BASED SLEEP FEATURE 🔥
# ---------------------------------------------------
@app.route("/face-sleep", methods=["POST"])
def face_sleep():
    data = request.get_json()

    age = data.get("age", 22)
    eye_closed_frames = data.get("eye_closed_frames", 0)

    fatigue_score = analyze_face(eye_closed_frames)
    sleep_hours = sleep_need_from_face(fatigue_score, age)

    return jsonify({
        "recommended_sleep_hours": sleep_hours,
        "fatigue_score": fatigue_score,
        "warning": (
            "High fatigue detected. Sleep 7–8 hours, reduce screen time."
            if fatigue_score > 60 else
            "Normal condition. Maintain healthy sleep routine."
        )
    })

# ---------------------------------------------------
# 5️⃣ ADVANCED FACE IMAGE ANALYSIS 🔥
# ---------------------------------------------------
@app.route("/analyze-face-image", methods=["POST"])
@require_auth
def analyze_face_image_route():
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
        
        image_data = data['image']
        user_info = request.current_user
        
        # Perform face analysis
        analysis_result = analyze_face_image(image_data, user_info)
        
        if analysis_result['success']:
            return jsonify({
                "success": True,
                "analysis": analysis_result['analysis'],
                "timestamp": analysis_result['timestamp']
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": analysis_result['error']
            }), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/face-analysis")
def face_analysis_page():
    return send_from_directory(FRONTEND_DIR, "face-analysis.html")


# ---------------------------------------------------
# RUN SERVER (ONLY ONCE ❗)
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
