import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(
    BASE_DIR,
    "scam_model.pkl"
)

with open(model_path, "rb") as f:
    model = pickle.load(f)

print("Scam model loaded successfully")


def predict_scam(email, title, description):

    text = f"{email} {title} {description}"

    prob = model.predict_proba([text])[0][1] * 100

    prob = round(prob, 2)

    if prob >= 80:
        label = "Scam"

    elif prob >= 45:
        label = "Medium Risk"

    else:
        label = "Legit"

    return prob, label