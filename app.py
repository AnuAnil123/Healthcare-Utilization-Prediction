from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # change this!
from sklearn.ensemble import GradientBoostingClassifier
import joblib

model = joblib.load('best_gbc_model.pkl')



# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Simple authentication
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')


import joblib
import pandas as pd

# Load the model and scaler globally (only once)
model = joblib.load('best_gbc_model.pkl')
scaler = joblib.load('scaler_gbc.joblib')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            features = ['age_2014', 'TrtOrder', 'LogAssets', 'health_worker_provides_',
                        'HHmembers_12', 'health_program_', 'FPrimary', 'weight']
            data = []

            for f in features:
                raw_val = request.form.get(f)
                if raw_val is None or raw_val.strip() == "":
                    raise ValueError(f"{f} is empty")
                val = float(raw_val)
                data.append(val)

            # Create DataFrame
            input_df = pd.DataFrame([data], columns=features)

            # Scale the data
            scaled_input = scaler.transform(input_df)

            # Make prediction
            prediction = model.predict(scaled_input)[0]

            # Convert prediction to label
            result = "Healthcare Sought" if prediction == 1 else "Healthcare Not Sought"

            return render_template('result.html', prediction=result)

        except ValueError as ve:
            flash(f"Invalid input: {ve}")
            return redirect(url_for('prediction'))

        except Exception as e:
            flash("Unexpected error occurred.")
            return redirect(url_for('prediction'))

    return render_template('prediction.html')




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

