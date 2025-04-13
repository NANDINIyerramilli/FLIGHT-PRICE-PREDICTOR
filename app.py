from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load the model
try:
    model = pickle.load(open("flight_rf.pkl", "rb"))
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

@app.route("/")
@cross_origin()
def home():
    """Render the home page"""
    return render_template("home.html")

def process_airline(airline):
    """Process airline input and return one-hot encoded values"""
    airlines = {
        'Jet Airways': 0, 'IndiGo': 1, 'Air India': 2, 
        'Multiple carriers': 3, 'SpiceJet': 4, 'Vistara': 5, 
        'GoAir': 6, 'Multiple carriers Premium economy': 7, 
        'Jet Airways Business': 8, 'Vistara Premium economy': 9, 
        'Trujet': 10
    }
    
    # Initialize all with zeros
    encoded = [0] * len(airlines)
    
    # Set the appropriate airline to 1
    if airline in airlines:
        encoded[airlines[airline]] = 1
        
    # Return values in the expected order
    return encoded[0], encoded[1], encoded[2], encoded[3], encoded[4], encoded[5], \
           encoded[6], encoded[7], encoded[8], encoded[9], encoded[10]

def process_source(source):
    """Process source input and return one-hot encoded values"""
    sources = {'Delhi': 0, 'Kolkata': 1, 'Mumbai': 2, 'Chennai': 3}
    
    # Initialize all with zeros
    encoded = [0] * len(sources)
    
    # Set the appropriate source to 1
    if source in sources:
        encoded[sources[source]] = 1
        
    # Return values in the expected order
    return encoded[0], encoded[1], encoded[2], encoded[3]

def process_destination(destination):
    """Process destination input and return one-hot encoded values"""
    destinations = {'Cochin': 0, 'Delhi': 1, 'New_Delhi': 2, 'Hyderabad': 3, 'Kolkata': 4}
    
    # Initialize all with zeros
    encoded = [0] * len(destinations)
    
    # Set the appropriate destination to 1
    if destination in destinations:
        encoded[destinations[destination]] = 1
        
    # Return values in the expected order
    return encoded[0], encoded[1], encoded[2], encoded[3], encoded[4]

def parse_datetime(date_str):
    """Parse datetime string and extract components"""
    dt = pd.to_datetime(date_str, format="%Y-%m-%dT%H:%M")
    return {
        'day': int(dt.day),
        'month': int(dt.month),
        'hour': int(dt.hour),
        'minute': int(dt.minute)
    }

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    """Handle prediction requests"""
    if request.method != "POST":
        return render_template("home.html")
    
    try:
        # Process date and time fields
        dep_dt = parse_datetime(request.form["Dep_Time"])
        arr_dt = parse_datetime(request.form["Arrival_Time"])
        
        # Calculate duration
        dur_hour = abs(arr_dt['hour'] - dep_dt['hour'])
        dur_min = abs(arr_dt['minute'] - dep_dt['minute'])
        
        # Get stops
        total_stops = int(request.form["stops"])
        
        # Process airline
        airline = request.form['airline']
        Jet_Airways, IndiGo, Air_India, Multiple_carriers, SpiceJet, Vistara, \
        GoAir, Multiple_carriers_Premium_economy, Jet_Airways_Business, \
        Vistara_Premium_economy, Trujet = process_airline(airline)
        
        # Process source
        source = request.form["Source"]
        s_Delhi, s_Kolkata, s_Mumbai, s_Chennai = process_source(source)
        
        # Process destination
        destination = request.form["Destination"]
        d_Cochin, d_Delhi, d_New_Delhi, d_Hyderabad, d_Kolkata = process_destination(destination)
        
        # Create feature array for prediction
        features = [
            total_stops, dep_dt['day'], dep_dt['month'], dep_dt['hour'], dep_dt['minute'],
            arr_dt['hour'], arr_dt['minute'], dur_hour, dur_min,
            Air_India, GoAir, IndiGo, Jet_Airways, Jet_Airways_Business,
            Multiple_carriers, Multiple_carriers_Premium_economy, SpiceJet, Trujet,
            Vistara, Vistara_Premium_economy, s_Chennai, s_Delhi, s_Kolkata, s_Mumbai,
            d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata, d_New_Delhi
        ]
        
        # Make prediction
        prediction = model.predict([features])
        output = round(prediction[0], 2)
        
        logger.info(f"Prediction made: Rs. {output}")
        return render_template('home.html', prediction_text=f"Your Flight price is Rs. {output}")
    
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        return render_template('home.html', prediction_text="Error processing your request. Please check your inputs.")

if __name__ == "__main__":
    app.run(debug=True)