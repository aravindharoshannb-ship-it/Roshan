import os
import re
import joblib

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_FILE = os.path.join(MODEL_DIR, "disaster_classifier.pkl")
VECTORIZER_FILE = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")


# ============================================================
# EMERGENCY KEYWORDS
# ============================================================

EMERGENCY_KEYWORDS = [
    "trapped",
    "urgent",
    "urgently",
    "emergency",
    "rescue",
    "rescue needed",
    "need rescue",
    "missing",
    "collapsed",
    "injured",
    "critical",
    "danger",
    "evacuate",
    "evacuation",
    "need help",
    "help needed"
]


# ============================================================
# RELIEF KEYWORDS
# ============================================================

RELIEF_KEYWORDS = [
    "relief",
    "relief camp",
    "relief materials",
    "food distribution",
    "medical camp",
    "aid distributed",
    "supplies distributed",
    "assistance provided"
]


# ============================================================
# DAMAGE KEYWORDS
# ============================================================

DAMAGE_KEYWORDS = [
    "damage",
    "destroyed",
    "damaged",
    "houses damaged",
    "roads damaged",
    "infrastructure damage",
    "loss",
    "destroyed houses",
    "property damage"
]


# ============================================================
# LOAD SAVED MODEL
# ============================================================

def load_models():

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            f"Classifier model not found:\n{MODEL_FILE}\n\n"
            "Please run classification.py once to train and save the model."
        )

    if not os.path.exists(VECTORIZER_FILE):
        raise FileNotFoundError(
            f"TF-IDF vectorizer not found:\n{VECTORIZER_FILE}\n\n"
            "Please run classification.py once to train and save the model."
        )

    classifier = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)

    return classifier, vectorizer


# ============================================================
# FIND KEYWORDS
# ============================================================

def detect_signals(message):

    text = message.lower()

    signals = []

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text:
            signals.append(keyword)

    return signals


# ============================================================
# CLASSIFY DISASTER MESSAGE
# ============================================================

def classify_message(message):

    if not message or not message.strip():
        return {
            "category": "General Information",
            "confidence": 0.0,
            "signals": []
        }

    text = message.strip()
    lower_text = text.lower()

    signals = detect_signals(text)

    # --------------------------------------------------------
    # Emergency rule
    # --------------------------------------------------------

    strong_emergency_keywords = [
        "trapped",
        "emergency",
        "rescue needed",
        "need rescue",
        "critical",
        "missing",
        "evacuate",
        "evacuation"
    ]

    strong_signal_found = any(
        keyword in lower_text
        for keyword in strong_emergency_keywords
    )

    if len(signals) >= 2:
        return {
            "category": "Emergency Request",
            "confidence": 0.95,
            "signals": signals
        }

    if strong_signal_found:
        return {
            "category": "Emergency Request",
            "confidence": 0.90,
            "signals": signals
        }

    # --------------------------------------------------------
    # Relief rule
    # --------------------------------------------------------

    relief_found = any(
        keyword in lower_text
        for keyword in RELIEF_KEYWORDS
    )

    if relief_found:
        return {
            "category": "Relief Update",
            "confidence": 0.90,
            "signals": signals
        }

    # --------------------------------------------------------
    # ML prediction
    # --------------------------------------------------------

    classifier, vectorizer = load_models()

    X = vectorizer.transform([text])

    prediction = classifier.predict(X)[0]

    confidence = 0.0

    if hasattr(classifier, "predict_proba"):
        probabilities = classifier.predict_proba(X)[0]
        confidence = float(max(probabilities))

    return {
        "category": prediction,
        "confidence": confidence,
        "signals": signals
    }


# ============================================================
# PRIORITY CLASSIFICATION
# ============================================================

def classify_priority(message):

    text = message.lower()

    high_keywords = [
        "trapped",
        "emergency",
        "urgent",
        "urgently",
        "rescue",
        "rescue needed",
        "critical",
        "missing",
        "collapsed",
        "danger",
        "evacuate",
        "evacuation"
    ]

    medium_keywords = [
        "injured",
        "damage",
        "damaged",
        "destroyed",
        "heavy rainfall",
        "flooding",
        "landslide",
        "storm"
    ]

    for keyword in high_keywords:
        if keyword in text:
            return "High"

    for keyword in medium_keywords:
        if keyword in text:
            return "Medium"

    return "Low"


# ============================================================
# TEST ONLY WHEN RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    sample_message = """
    Severe flooding has affected several houses in Coimbatore.
    Five people are trapped and residents urgently need food and
    medical assistance. Rescue teams are requested immediately.
    """

    result = classify_message(sample_message)
    priority = classify_priority(sample_message)

    print("\n====================================")
    print("HYBRID DISASTER CLASSIFICATION")
    print("====================================")

    print("\nMessage:")
    print(sample_message)

    print("\nPredicted Category:")
    print(result["category"])

    print("\nConfidence:")
    print(round(result["confidence"] * 100, 2), "%")

    print("\nPriority:")
    print(priority)

    print("\nDetected Signals:")
    print(result["signals"])
