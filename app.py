from flask import Flask, render_template
import moisture
from datetime import datetime
import threading
import csv

app = Flask(__name__)


vera_öntözve = ""
fikusz_öntözve = ""

plant1 = []
plant2 = []

def load_data():
    plant1 = []
    plant2 = []
    with open("sensor_data.csv", "r") as file:
        data = csv.reader(file)
        for row in data:
            time = row[1].strip()
            sensor_value1 = row[2].strip()
            sensor_value2 = row[3].strip()
            plant1.append([float(time), int(sensor_value1)])
            plant2.append([float(time), int(sensor_value2)])

        return plant1, plant2

@app.route('/', methods=["GET", "POST"])
def main():
    global plant1, plant2
    plant1 = load_data()[0]
    plant2 = load_data()[1]
    try:
        adat1 = plant1[-100:]
        adat2 = plant2[-100:]
    except:
        adat1 = plant1
        adat2 = plant2

    return render_template('index.html', adat1 = adat1, adat2 = adat2)

@app.route('/watering_vera', methods=["GET", "POST"])
def watering_vera():

    global vera_öntözve
    vera_öntözve = "Utoljára öntözve {}".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    moisture.ser.write(bytes(b"v"))

    return render_template('index.html',adat1 = plant1[-100:], adat2 = plant2[-100:], vera_öntözve = vera_öntözve, fikusz_öntözve = fikusz_öntözve)

@app.route('/watering_fikusz', methods=["GET", "POST"])
def watering_fikusz():

    global fikusz_öntözve
    fikusz_öntözve = "Utoljára öntözve {}".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    moisture.ser.write(bytes(b"f"))

    return render_template('index.html',adat1 = plant1[-100:], adat2 = plant2[-100:], vera_öntözve = vera_öntözve, fikusz_öntözve = fikusz_öntözve)

def gather_data():
    while True:
        try:
            moisture.get_moisture()
        except Exception as e:
            print(e)
            continue

def runApp():
    app.run(host="0.0.0.0", debug=True, use_reloader=False)

if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=runApp).start()
        t2 = threading.Thread(target=gather_data).start()
    except Exception as e:
        print(e)


