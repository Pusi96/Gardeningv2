from flask import Flask, render_template
import moisture
from datetime import datetime
import threading

app = Flask(__name__)

plant1 = []
plant2 = []

@app.route('/', methods=["GET", "POST"])
def main():
    try:
        adat1 = plant1[-100:]
        adat2 = plant2[-100:]
    except:
        adat1 = plant1
        adat2 = plant2

    return render_template('index.html', adat1 = adat1, adat2 = adat2)

vera_öntözve = ""
fikusz_öntözve = ""

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
    last_time = datetime.now()
    while True:
        try:
            data = moisture.get_moisture()
            time = data[0]
            sensor1 = data[1]
            sensor2 = data[2]

            plant1_point = [time, sensor1]
            plant2_point = [time, sensor2]
            plant1.append(plant1_point)
            plant2.append(plant2_point)

            now = datetime.now()
            elapsed_time = now - last_time
            last_time = now
            print(elapsed_time)

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


