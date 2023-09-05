from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Define the list of cities (you can modify this list as needed)
cities = [
    "Vancouver",
    "Calgary",
    "Edmonton",
    "Winnipeg",
    "Saskatoon",
    "Victoria"

]

def load_city_data_from_csv():
    city_data = {}
    with open('data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            city_name = row['city']
            city_data[city_name] = row
    return city_data

city_data = load_city_data_from_csv()

def load_city_data(city):
    if city in city_data:
        return city_data[city]
    else:
        return {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_city = request.form['city']
        selected_city_data = load_city_data(selected_city)
        return render_template('index.html', cities=cities, city_data=selected_city_data)
    
    return render_template('index.html', cities=cities, city_data=None)

@app.route('/get_dashboard', methods=['POST'])
def get_dashboard():
    data = request.get_json()  # Get the selected city from the request
    selected_city = data['city']
    selected_city_data = load_city_data(selected_city)
    return jsonify(selected_city_data)  # Return the city data as JSON

if __name__ == '__main__':
    app.run()
