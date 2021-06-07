from datetime import datetime
import csv
import serial
from time import time

ser = serial.Serial('COM3', 9600, timeout = None) # for Windows port
#ser = serial.Serial("/dev/ttyACM0",9600, timeout = None) # for Arduino port

def get_moisture():

        try:
                moisture1 = int(ser.readline().decode().rstrip().split(',')[0])
                moisture2 = int(ser.readline().decode().rstrip().split(',')[1])

        except Exception as e:
                print(e)

        data_to_save = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), time()*1000 + 7200*1000, moisture1, moisture2]
        data = [time()*1000 + 7200*1000, moisture1, moisture2]

        with open("sensor_data.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(data_to_save)

        return data

