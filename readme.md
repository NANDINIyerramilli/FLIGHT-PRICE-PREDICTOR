
   FLIGHT PRICE PREDICTOR
A machine learning-powered web application that predicts flight fares based on input features like airline, source, destination, journey date, time, and stops. Built using Flask for the backend and a trained Random Forest Regressor model for predictions.



   Demo
   
![Screenshot 2025-04-13 194011](https://github.com/user-attachments/assets/96ccb048-eb2e-46f7-b389-5bd5b86f6f13)



   Project Structure

FLIGHT-PRICE-PREDICTOR/
├── static/css/               # Styling for the web app
│   └── style.css
├── template/                 # HTML templates
│   └── home.html
├── README.md                 # Project documentation
├── app.py                    # Flask backend
├── flight_price.ipynb        # Model training and analysis notebook
├── flight_rf.pkl(.gitattribures) # Trained Random Forest model
├── requirements.txt          # Project dependencies
├── Data_Train.xlsx           # Training dataset
├── Test_set.xlsx             # Test dataset


  Features
- Predicts flight fare based on user input
- Interactive web interface
- Backend powered by a machine learning model
- Clean and easy-to-use UI



  Model Details
- Libraries: scikit-learn, pandas, numpy
- Features Used:
  - Airline
  - Source & Destination
  - Total Stops
  - Journey Date, Departure & Arrival Time
  - Duration
  - Additional Information

Model training is done in the `flight_price.ipynb` notebook, and the trained model is saved as `flight_rf.pkl`.


   How to Run Locally
1. Clone the Repository
   git clone https://github.com/yourusername/FLIGHT-PRICE-PREDICTOR.git
   cd FLIGHT-PRICE-PREDICTOR
2. Install Dependencies
   pip install -r requirements.txt
3. Run the App
   python app.py
5. Open in Browser
  

   Requirements
Key libraries listed in requirements.txt:
- Flask
- scikit-learn
- pandas
- numpy


-Contributions
Have suggestions or improvements? Fork the repo and submit a pull request!

-License
Open-source under the MIT License.

-Author
Created by [Nandini Y](https://github.com/NANDINIyerramilli)
