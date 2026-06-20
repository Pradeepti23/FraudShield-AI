# ==========================================================
# FRAUDSHIELD-AI
# APP.PY
# Credit Card Fraud Detection System
# Random Forest + XGBoost
# ==========================================================

# ==========================================================
# IMPORTS
# ==========================================================
from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

from database import (
    create_transactions_table,
    save_transaction,
    get_dashboard_stats,
    get_all_transactions
)

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================
create_transactions_table()

# ==========================================================
# FLASK APP
# ==========================================================
app = Flask(__name__)
app.secret_key = "fraudshield_secret_key"

# ==========================================================
# LOAD MODELS
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:

    rf_model = joblib.load(
        os.path.join(BASE_DIR, "model", "random_forest_fraud.pkl")
    )

    xgb_model = joblib.load(
        os.path.join(BASE_DIR, "model", "xgboost_fraud.pkl")
    )

    scaler = joblib.load(
        os.path.join(BASE_DIR, "model", "scaler.pkl")
    )

    encoders = joblib.load(
        os.path.join(BASE_DIR, "model", "label_encoders.pkl")
    )

    print("✅ Models Loaded Successfully")

except Exception as e:

    print("❌ MODEL LOAD ERROR")
    print(e)

    rf_model = None
    xgb_model = None
    scaler = None
    encoders = {}

# ==========================================================
# HOME PAGE
# ==========================================================
@app.route("/")
def home():

    return render_template("index.html")


# ==========================================================
# DASHBOARD PAGE
# ==========================================================
@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()

    return render_template(
        "dashboard.html",
        total_transactions=stats["total"],
        fraud_count=stats["fraud"],
        genuine_count=stats["genuine"],
        detection_rate=stats["fraud_rate"]
    )


# ==========================================================
# PREDICTION PAGE
# ==========================================================
@app.route("/predict", methods=["GET", "POST"])
def predict():

    result = None
    probability = None
    risk_score = None

    if request.method == "POST":

        try:

            # ==================================================
            # GET INPUT FROM FORM
            # ==================================================
            data = pd.DataFrame([{
                "transaction_amount": float(request.form["transaction_amount"]),
                "transaction_type": request.form["transaction_type"],
                "merchant_category": request.form["merchant_category"],
                "transaction_time": request.form["transaction_time"],
                "customer_age": int(request.form["customer_age"]),
                "previous_fraud_history": request.form["previous_fraud_history"],
                "new_device_used": request.form["new_device_used"],
                "international_transaction": request.form["international_transaction"],
                "location_match": request.form["location_match"],
                "transactions_today": int(request.form["transactions_today"])
            }])

            # ==================================================
            # FEATURE ENGINEERING
            # ==================================================
            data["amount_category"] = pd.cut(
                data["transaction_amount"],
                bins=[0, 1000, 10000, 50000, 100000],
                labels=["Low", "Medium", "High", "Very_High"]
            )

            data["high_amount_flag"] = (
                data["transaction_amount"] > 50000
            ).astype(int)

            data["high_frequency_flag"] = (
                data["transactions_today"] > 10
            ).astype(int)

            data["new_device_risk"] = (
                data["new_device_used"] == "Yes"
            ).astype(int)

            data["international_risk"] = (
                data["international_transaction"] == "Yes"
            ).astype(int)

            data["location_risk"] = (
                data["location_match"] == "No"
            ).astype(int)

            data["history_risk"] = (
                data["previous_fraud_history"] == "Yes"
            ).astype(int)

            data["risk_score"] = (
                data["high_amount_flag"]
                + data["high_frequency_flag"]
                + data["new_device_risk"]
                + data["international_risk"]
                + data["location_risk"]
                + data["history_risk"]
            )

            risk_score = int(data["risk_score"].iloc[0])

            # ==================================================
            # LABEL ENCODING
            # ==================================================
            for col, encoder in encoders.items():

                if col in data.columns:

                    try:
                        data[col] = encoder.transform(data[col])

                    except:
                        data[col] = 0

            # ==================================================
            # MATCH TRAINING COLUMNS
            # ==================================================
            data = data.reindex(
                columns=scaler.feature_names_in_,
                fill_value=0
            )

            # ==================================================
            # SCALING
            # ==================================================
            scaled_data = scaler.transform(data)

            # ==================================================
            # MODEL PREDICTION
            # ==================================================
            active_model = rf_model if rf_model is not None else xgb_model

            prediction = active_model.predict(scaled_data)[0]

            probability = round(
                active_model.predict_proba(scaled_data)[0][1] * 100,
                2
            )

            # ==================================================
            # RESULT
            # ==================================================
            result = "Fraud" if prediction == 1 else "Genuine"

            # ==================================================
            # SAVE TO DATABASE
            # ==================================================
            save_transaction(
                amount=float(request.form["transaction_amount"]),
                transaction_type=request.form["transaction_type"],
                merchant_category=request.form["merchant_category"],
                result=result,
                probability=probability,
                risk_score=risk_score
            )

        except Exception as e:

            print("Prediction Error:", e)

            return render_template(
                "predict.html",
                error=str(e)
            )

    return render_template(
        "predict.html",
        prediction=result,
        probability=probability,
        risk_score=risk_score
    )


# ==========================================================
# HISTORY PAGE
# ==========================================================
@app.route("/history")
def history():

    transactions = get_all_transactions()

    return render_template(
        "history.html",
        transactions=transactions
    )


# ==========================================================
# RUN APPLICATION
# ==========================================================
if __name__ == "__main__":

    app.run(
        debug=True
    )