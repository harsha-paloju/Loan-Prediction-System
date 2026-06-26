from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)


model = joblib.load("best_rf.pkl")


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():

    

    gender = request.form["gender"]
    married = request.form["married"]
    dependents = request.form["dependents"]
    education = request.form["education"]
    self_employed = request.form["self_employed"]

    applicant_income = float(request.form["applicant_income"])
    coapplicant_income = float(request.form["coapplicant_income"])

    loan_amount = float(request.form["loan_amount"])
    loan_amount_term = float(request.form["loan_amount_term"])

    credit_history = int(request.form["credit_history"])

    property_area = request.form["property_area"]

    

    gender = 1 if gender == "Male" else 0

    married = 1 if married == "Yes" else 0

    education = 1 if education == "Graduate" else 0

    self_employed = 1 if self_employed == "Yes" else 0

    dependents = int(dependents)

   

    total_income = applicant_income + coapplicant_income

    loan_income_ratio = loan_amount / total_income

    

    property_area_semiurban = 0
    property_area_urban = 0

    if property_area == "Semiurban":
        property_area_semiurban = 1

    elif property_area == "Urban":
        property_area_urban = 1

    

    sample = pd.DataFrame([{

        "Gender": gender,

        "Married": married,

        "Dependents": dependents,

        "Education": education,

        "Self_Employed": self_employed,

        "ApplicantIncome": applicant_income,

        "CoapplicantIncome": coapplicant_income,

        "LoanAmount": loan_amount,

        "Loan_Amount_Term": loan_amount_term,

        "Credit_History": credit_history,

        "TotalIncome": total_income,

        "LoanIncomeRatio": loan_income_ratio,

        "Property_Area_Semiurban": property_area_semiurban,

        "Property_Area_Urban": property_area_urban

    }])

    

    prediction = model.predict(sample)[0]

    probability = model.predict_proba(sample)[0]

    approval_probability = round(probability[1] * 100, 2)

    rejection_probability = round(probability[0] * 100, 2)

    

    if prediction == 1:

        status = "Approved"

        confidence = approval_probability

    else:

        status = "Rejected"

        confidence = rejection_probability

    return render_template(

        "result.html",

        prediction=status,

        confidence=confidence

    )



if __name__ == "__main__":
    app.run(debug=True)