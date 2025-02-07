import time
from BMP280_i2c_sensor.get_temperature_reading__init__ import bmp280_temperature


def i2c_averaging():
    """
    Reads temperature data from the BMP280 sensor and calculates the average.
    """

    try:
        samplespm = int(input("Input samples per minute: "))
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
        exit(1)  

    sensor = bmp280_temperature()  

    try: 
        delay = 60 / samplespm
        while True:
            count = 0
            sum_temperature = 0
         
            while count < samplespm:  
                sum_temperature += sensor.sample_i2c_temperature()
                count += 1
                time.sleep(delay)
      
            average_temp = sum_temperature / samplespm
            print(f"Average temperature = {average_temp:.2f}°C")
            
    except ValueError:
        print("Invalid input. Enter a positive integer.")