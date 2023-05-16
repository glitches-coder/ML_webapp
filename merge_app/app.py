from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

# Load the .pkl models here
model1 = joblib.load('energy_model.pkl')
model2 = joblib.load('energy_mlr_model.pkl')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    power = float(request.form['power'])
    voltage = float(request.form['voltage'])
    temperature = float(request.form.get('temperature', 0))
    humidity = float(request.form.get('humidity', 0))
    time = float(request.form['time'])
    model_name = request.form['model']
    
    # Use the appropriate model to make a prediction
    if model_name == 'model1':
        model = model1
        prediction = model.predict([[power, voltage, time]])
    elif model_name == 'model2':
        model = model2
        prediction = model.predict([[power, voltage, temperature, humidity, time]])
    else:
        return 'Invalid model name'
    
    energy_consumed_wh = prediction[0]  # Energy consumption in watt-hours
    energy_consumed_kwh = energy_consumed_wh / 1000  # Convert to kilowatt-hours
    cost = energy_consumed_kwh * 2.5  # Tariff slab of 2.5 rupees per kilowatt-hour
    
    return render_template('result.html', prediction=energy_consumed_kwh, cost=cost, model=model_name)

if __name__ == '__main__':
    app.run(debug=True)





