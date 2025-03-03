import time
from raspi_temperature_driver.temperature_class import DeviceTemperature
from i2c_devices.BMP280_i2c_sensor.bmp280_temperature import Bmp280
from i2c_devices.BMP280_i2c_sensor.bmp280_humidity import Bmp280Humidity


def average_temp_per_minute(device_temperature:
    DeviceTemperature = None, i2c_bus=None, address=None):
    """gets bus, address, creates temperature sensor object,
    takes input and samples temp/ humidity this many times per minute

    Args:
        DeviceTemperature retrieves the raspberry pi temp. 
        device_temperature Defaults to None.
    """

    if device_temperature is None:
        device_temperature = DeviceTemperature()

    samplespm = int(input("Input samples per minute: "))
    if samplespm <= 0:
        print("Invalid input. Please enter a positive integer.")
        return


    bmp = Bmp280(i2c_bus, address) # create temperature sensor
    humidity_sensor = Bmp280Humidity(i2c_bus, address, bmp) # create humidity sensor

    delay = 60 / samplespm
    while True:
        start_time = time.time()  # Start time tracking

        sum_temperature1 = 0
        sum_temperature2 = 0
        sum_humidity3 = 0

        for _ in range(samplespm):

            sum_temperature1 += bmp.read_temperature()
            sum_temperature2 += device_temperature.read_cpu_temperature()
            sum_humidity3 += humidity_sensor.read_humidity()
            time.sleep(delay)


        elapsed_time = time.time() - start_time  # Total loop time

        average_temp_i2c = sum_temperature1 / samplespm
        average_temp_raspi = sum_temperature2 / samplespm
        average_humid_i2c = sum_humidity3 / samplespm

        print(f"Average I2C CPU Temp = {average_temp_i2c:.2f}°C")
        print(f"Average Raspberry Pi CPU Temp = {average_temp_raspi:.2f}°C")
        print(f"Average I2C Humidity = {average_humid_i2c:.2f}%RH")


        # Adjust the sleep time so that total duration is as close to 60s as possible
        remaining_time = 60 - elapsed_time
        if remaining_time > 0:
            time.sleep(remaining_time)
