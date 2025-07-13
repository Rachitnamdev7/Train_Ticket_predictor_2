from flask import Flask, render_template, request
import pandas as pd
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)

# Load model and encoders
model = joblib.load("model.pkl")
train_encoder = joblib.load("train_no_encoder.pkl")
class_encoder = joblib.load("class_encoder.pkl")
status_encoder = joblib.load("status_encoder.pkl")

# Load route data
df = pd.read_csv("train_data.csv")
df.columns = df.columns.str.strip().str.lower()

def fetch_trains_between(source, destination, date):
    source = source.strip().upper()
    destination = destination.strip().upper()

    valid_trains = set()
    for _, row in df.iterrows():
        train_no = str(row['train_no']).strip()
        src = row['source'].strip().upper()
        dest = row['destination'].strip().upper()
        inter = [s.strip().upper() for s in row['intermideate'].split(",")]

        # check route order: source → intermediate stations → destination
        if source == src and destination == dest:
            valid_trains.add(train_no)
        elif source in inter and destination in inter:
            if inter.index(source) < inter.index(destination):
                valid_trains.add(train_no)
        elif source == src and destination in inter:
            valid_trains.add(train_no)
        elif source in inter and destination == dest:
            valid_trains.add(train_no)

    trains = [{"train_no": train, "train_name": f"Train {train}"} for train in valid_trains]
    return trains

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/select_train', methods=['POST'])
def select_train():
    source = request.form['source'].strip().upper()
    destination = request.form['destination'].strip().upper()
    journey_date = request.form['journey_date']

    trains = fetch_trains_between(source, destination, journey_date)

    if not trains:
        return render_template("select_train.html", trains=[], source=source,
                               destination=destination, journey_date=journey_date, error="No trains found.")

    return render_template("select_train.html", trains=trains, source=source,
                           destination=destination, journey_date=journey_date)

@app.route('/passenger_details', methods=['POST'])
def passenger_details():
    train_no = request.form['train_no']
    train_name = request.form['train_name']
    source = request.form['source']
    destination = request.form['destination']
    journey_date = request.form['journey_date']

    return render_template("passenger_form.html",
                           train_no=train_no,
                           train_name=train_name,
                           source=source,
                           destination=destination,
                           journey_date=journey_date)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        train_no = request.form['train_no']
        train_name = request.form['train_name']
        source = request.form['source']
        destination = request.form['destination']
        journey_date = request.form['journey_date']
        travel_class = request.form['class']
        passengers = int(request.form['passengers'])
        wl_first = int(request.form['wl_first'])

        booking_date = datetime.today().date()
        journey_dt = datetime.strptime(journey_date, "%Y-%m-%d").date()

        train_encoded = train_encoder.transform([train_no])[0]
        class_encoded = class_encoder.transform([travel_class])[0]

        predictions = []

        for i in range(5):
            date_i = journey_dt + timedelta(days=i)
            gap = (date_i - booking_date).days
            wl = wl_first
            daily_predictions = []

            # First passenger prediction
            input_df = pd.DataFrame([[
                train_encoded, class_encoded, 0, wl, gap
            ]], columns=['train_no', 'class', 'avl', 'wl', 'days_gap'])

            probs = model.predict_proba(input_df)[0]
            confirm_idx = list(status_encoder.classes_).index('confirmed')
            first_percent = round(probs[confirm_idx] * 100, 2)

            for p in range(passengers):
                if p == 0:
                    percent = first_percent
                else:
                    # reduce based on 1.5% of first passenger's prediction
                    percent = max(0, round(first_percent - (p * 0.015 * first_percent), 2))
                daily_predictions.append({
                    "passenger": p + 1,
                    "wl": wl,
                    "percent": percent
                })
                wl += 1  # Increase WL for each passenger

            predictions.append({
                "date": date_i.strftime("%Y-%m-%d"),
                "results": daily_predictions
            })

        return render_template("result.html", predictions=predictions)

    except Exception as e:
        return render_template("result.html", error=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
