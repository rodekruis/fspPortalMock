import pandas as pd
import random
import io
import os
from flask import Flask, render_template, request, send_file, flash

# Fetch portal name from environment variable or use a default value
portal_name = os.environ['PORTAL_NAME']
if portal_name is None:
    portal_name = 'Bank Payment Portal'

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

def process_csv(csv_file):
    # Load CSV file into pandas DataFrame with automatic delimiter detection
    try:
        df = pd.read_csv(csv_file, sep=None, engine='python')  # Automatically detect delimiter
    except Exception as e:
        flash(f"Error parsing CSV file: {str(e)}")
        return None

    # Check if 'id' and 'amount' columns exist
    if 'id' not in df.columns or 'amount' not in df.columns:
        flash("Error: 'id' or 'amount' column is missing.")
        return None

    # Check for non-unique values in the 'id' column
    if df['id'].nunique() != len(df):
        flash("Error: 'id' column contains non-unique values.")
        return None

    # Add 'status' column with random distribution of 'success' and 'error'
    error_rate = round(random.uniform(0.01,0.05),2)
    df['status'] = ['error' if random.random() <= error_rate else 'success' for _ in range(len(df))]

    # Randomly delete between 1 and 3 rows
    rows_to_delete = random.randint(1, 3)
    if rows_to_delete > 0:
        indices = random.sample(range(len(df)), rows_to_delete)
        df = df.drop(indices)

    return df

@app.route('/')
def index():
    return render_template('index.html', portal_name=portal_name)

@app.route('/upload', methods=['POST'])
def upload():
    if 'csv_file' not in request.files:
        flash("Error: No file part.")
        return render_template('index.html')

    file = request.files['csv_file']
    if file.filename == '':
        flash("Error: No selected file.")
        return render_template('index.html')

    if file:
        df = process_csv(file)
        if df is None:
            return render_template('index.html')
        
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(output, mimetype='text/csv', download_name='reconciliation_report.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
