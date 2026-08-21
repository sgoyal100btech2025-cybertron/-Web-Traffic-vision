from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    jsonify,
    send_file
)

import pandas as pd
import sqlite3
import plotly.express as px
import plotly
import json
import joblib
import os
import numpy as np

from datetime import timedelta
from werkzeug.utils import secure_filename

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# =====================================================
# APP CONFIG
# =====================================================

app = Flask(__name__)

app.secret_key = "trafficvision_secret_key"

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('models', exist_ok=True)

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(
    'trafficvision.db',
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    predicted_visitors INTEGER
)
''')

conn.commit()

# =====================================================
# DATASET CONFIG
# =====================================================

DATASET_PATH = 'dataset.csv'

# =====================================================
# COLUMN ALIASES
# =====================================================

DATE_COLUMN_ALIASES = [

    'date',
    'day',
    'time',
    'timestamp',
    'datetime',
    'created_at',
    'record_date',
    'dates',
    'event_date'

]

VISITOR_COLUMN_ALIASES = [

    'visitors',
    'traffic',
    'users',
    'website_users',
    'hits',
    'views',
    'pageviews',
    'sessions',
    'count',
    'audience',
    'visitor_count',
    'website_traffic'

]

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def allowed_file(filename):

    return (
        '.' in filename
        and
        filename.rsplit('.', 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

def smart_load_csv(filepath):

    try:

        # ============================================
        # READ CSV
        # ============================================

        try:

            temp_df = pd.read_csv(
                filepath,
                encoding='utf-8'
            )

        except:

            try:

                temp_df = pd.read_csv(
                    filepath,
                    sep=';',
                    encoding='utf-8'
                )

            except:

                temp_df = pd.read_csv(
                    filepath,
                    encoding='latin1'
                )

        # ============================================
        # CLEAN COLUMN NAMES
        # ============================================

        cleaned_columns = []

        for col in temp_df.columns:

            cleaned = str(col)

            cleaned = cleaned.strip()

            cleaned = cleaned.lower()

            cleaned = cleaned.replace(" ", "_")

            cleaned = cleaned.replace("-", "_")

            cleaned = cleaned.replace(".", "_")

            cleaned = cleaned.replace("\ufeff", "")

            cleaned_columns.append(cleaned)

        temp_df.columns = cleaned_columns

        print("\n========== CLEANED COLUMNS ==========")
        print(temp_df.columns.tolist())
        print("=====================================\n")

        # ============================================
        # DETECT DATE COLUMN
        # ============================================

        detected_date_col = None

        for col in temp_df.columns:

            if any(alias in col for alias in DATE_COLUMN_ALIASES):

                detected_date_col = col
                break

        # SMART DATE DETECTION

        if detected_date_col is None:

            for col in temp_df.columns:

                try:

                    converted = pd.to_datetime(
                        temp_df[col],
                        errors='coerce'
                    )

                    valid_dates = converted.notna().sum()

                    if valid_dates >= len(temp_df) * 0.5:

                        detected_date_col = col
                        break

                except:
                    pass

        # ============================================
        # DETECT VISITOR COLUMN
        # ============================================

        detected_visitor_col = None

        for col in temp_df.columns:

            if any(alias in col for alias in VISITOR_COLUMN_ALIASES):

                detected_visitor_col = col
                break

        # SMART NUMERIC DETECTION

        if detected_visitor_col is None:

            for col in temp_df.columns:

                try:

                    numeric_values = pd.to_numeric(
                        temp_df[col],
                        errors='coerce'
                    )

                    valid_numeric = numeric_values.notna().sum()

                    if valid_numeric >= len(temp_df) * 0.5:

                        detected_visitor_col = col
                        break

                except:
                    pass

        print("Detected DATE column:", detected_date_col)
        print("Detected VISITOR column:", detected_visitor_col)

        # ============================================
        # VALIDATION
        # ============================================

        if detected_date_col is None:

            raise Exception(
                "AI could not detect DATE column."
            )

        if detected_visitor_col is None:

            raise Exception(
                "AI could not detect VISITOR column."
            )

        # ============================================
        # CREATE STANDARD COLUMNS
        # ============================================

        temp_df['date'] = pd.to_datetime(
            temp_df[detected_date_col],
            errors='coerce'
        )

        temp_df['visitors'] = pd.to_numeric(
            temp_df[detected_visitor_col],
            errors='coerce'
        )

        # ============================================
        # KEEP REQUIRED COLUMNS
        # ============================================

        temp_df = temp_df[[
            'date',
            'visitors'
        ]]

        # ============================================
        # CLEAN DATA
        # ============================================

        temp_df.dropna(inplace=True)

        temp_df.drop_duplicates(inplace=True)

        temp_df = temp_df.sort_values(
            by='date'
        )

        temp_df.reset_index(
            drop=True,
            inplace=True
        )

        # ============================================
        # CREATE DAY COLUMN
        # ============================================

        temp_df['day'] = range(
            1,
            len(temp_df) + 1
        )

        # ============================================
        # FINAL VALIDATION
        # ============================================

        if len(temp_df) < 5:

            raise Exception(
                "Dataset must contain at least 5 valid rows."
            )

        return temp_df

    except Exception as e:

        raise Exception(
            f"CSV Processing Error: {str(e)}"
        )
# =====================================================
# LOAD DATASET
# =====================================================

try:

    df = smart_load_csv(DATASET_PATH)

except Exception as e:

    print(e)

    sample_df = pd.DataFrame({

        'date': pd.date_range(
            start='2026-01-01',
            periods=30
        ),

        'visitors': np.random.randint(
            1000,
            5000,
            30
        )

    })

    sample_df['day'] = range(
        1,
        len(sample_df) + 1
    )

    sample_df.to_csv(
        DATASET_PATH,
        index=False
    )

    df = sample_df

# =====================================================
# TRAIN MODELS
# =====================================================

def train_models():

    global linear_model
    global rf_model

    X = df[['day']]
    y = df['visitors']

    linear_model = LinearRegression()

    linear_model.fit(X, y)

    rf_model = RandomForestRegressor(

        n_estimators=150,
        random_state=42

    )

    rf_model.fit(X, y)

    joblib.dump(
        linear_model,
        'models/linear_model.pkl'
    )

    joblib.dump(
        rf_model,
        'models/rf_model.pkl'
    )

train_models()

# =====================================================
# DASHBOARD CHART
# =====================================================

def generate_dashboard_chart():

    fig = px.line(

        df,

        x='date',
        y='visitors',

        markers=True,

        template='plotly_dark',

        title='Website Traffic Analytics'

    )

    fig.update_layout(

        paper_bgcolor='#0f172a',
        plot_bgcolor='#0f172a',

        font=dict(color='white'),

        title_font_size=24

    )

    return json.dumps(
        fig,
        cls=plotly.utils.PlotlyJSONEncoder
    )

# =====================================================
# HOME
# =====================================================

@app.route('/')
def index():

    current_visitors = int(
        df['visitors'].iloc[-1]
    )

    growth = round(

        (
            (
                df['visitors'].iloc[-1]
                -
                df['visitors'].iloc[0]
            )

            /
            df['visitors'].iloc[0]

        ) * 100,

        2

    )

    average_visitors = int(
        df['visitors'].mean()
    )

    peak_traffic = int(
        df['visitors'].max()
    )

    lowest_traffic = int(
        df['visitors'].min()
    )

    total_days = len(df)

    graphJSON = generate_dashboard_chart()

    return render_template(

        'dashboard.html',

        graphJSON=graphJSON,

        current_visitors=current_visitors,

        growth=growth,

        average_visitors=average_visitors,

        peak_traffic=peak_traffic,

        lowest_traffic=lowest_traffic,

        total_days=total_days

    )

# =====================================================
# PREDICT
# =====================================================

@app.route('/predict')
def predict():

    future_days = []
    predictions = []

    last_day = df['day'].max()

    for i in range(1, 11):

        future_day = last_day + i

        lr_pred = linear_model.predict(
            [[future_day]]
        )[0]

        rf_pred = rf_model.predict(
            [[future_day]]
        )[0]

        final_pred = int(
            (lr_pred + rf_pred) / 2
        )

        future_date = (

            df['date'].max()
            + timedelta(days=i)

        ).strftime('%Y-%m-%d')

        future_days.append(future_date)
        predictions.append(final_pred)

        cursor.execute(

            '''
            INSERT INTO history
            (date, predicted_visitors)
            VALUES (?, ?)
            ''',

            (future_date, final_pred)

        )

    conn.commit()

    pred_df = pd.DataFrame({

        'date': future_days,
        'predictions': predictions

    })

    fig = px.line(

        pred_df,

        x='date',
        y='predictions',

        markers=True,

        template='plotly_dark',

        title='AI Traffic Forecast'

    )

    fig.update_layout(

        paper_bgcolor='#0f172a',
        plot_bgcolor='#0f172a',

        font=dict(color='white'),

        title_font_size=24

    )

    pred_graph = json.dumps(

        fig,

        cls=plotly.utils.PlotlyJSONEncoder

    )

    results = list(
        zip(future_days, predictions)
    )

    return render_template(

        'index.html',

        results=results,

        pred_graph=pred_graph

    )

# =====================================================
# HISTORY
# =====================================================

@app.route('/history')
def history():

    cursor.execute(

        '''
        SELECT *
        FROM history
        ORDER BY id DESC
        '''

    )

    rows = cursor.fetchall()

    return render_template(
        'history.html',
        rows=rows
    )

# =====================================================
# CLEAR HISTORY
# =====================================================

@app.route('/clear-history')
def clear_history():

    cursor.execute(
        'DELETE FROM history'
    )

    conn.commit()

    flash(
        'Prediction history cleared successfully!',
        'success'
    )

    return redirect('/history')

# =====================================================
# EXPORT HISTORY
# =====================================================

@app.route('/export-history')
def export_history():

    query = '''
    SELECT *
    FROM history
    '''

    history_df = pd.read_sql_query(
        query,
        conn
    )

    export_path = 'prediction_history.csv'

    history_df.to_csv(
        export_path,
        index=False
    )

    return send_file(
        export_path,
        as_attachment=True
    )

# =====================================================
# API
# =====================================================

@app.route('/api/predictions')
def api_predictions():

    cursor.execute(

        '''
        SELECT *
        FROM history
        ORDER BY id DESC
        LIMIT 10
        '''

    )

    rows = cursor.fetchall()

    data = []

    for row in rows:

        data.append({

            "id": row[0],
            "date": row[1],
            "predicted_visitors": row[2]

        })

    return jsonify(data)

# =====================================================
# CSV UPLOAD
# =====================================================

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    global df

    if request.method == 'POST':

        if 'file' not in request.files:

            flash(
                'No file selected!',
                'danger'
            )

            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':

            flash(
                'Please select a CSV file!',
                'warning'
            )

            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(
                file.filename
            )

            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            file.save(filepath)

            try:

                uploaded_df = smart_load_csv(
                    filepath
                )

                df = uploaded_df

                df.to_csv(
                    DATASET_PATH,
                    index=False
                )

                train_models()

                flash(

                    'Dataset uploaded and AI models retrained successfully!',

                    'success'

                )

                return redirect('/')

            except Exception as e:

                flash(
                    str(e),
                    'danger'
                )

                return redirect(request.url)

        else:

            flash(
                'Only CSV files are allowed!',
                'danger'
            )

            return redirect(request.url)

    return render_template(
        'upload.html'
    )

# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':

    app.run(

        debug=True,

        host='0.0.0.0',

        port=5000

    )