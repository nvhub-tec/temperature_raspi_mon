import time
from smbus2 import SMBus
from raspi_temperature_driver.temperature_class import DeviceTemperature
from i2c_devices.BMP280_i2c_sensor.bmp280 import Bmp280
from i2c_devices.BMP280_i2c_sensor.get_bus_and_address import find_i2c_bus, find_i2c_address


def average_temp_per_minute(device_temperature: DeviceTemperature = None):
    
    if device_temperature is None:
        device_temperature = DeviceTemperature()

    samplespm = int(input("Input samples per minute: "))
    if samplespm <= 0:
        print("Invalid input. Please enter a positive integer.")
        return
    bus_number = find_i2c_bus()  # Get I2C bus number
    address = find_i2c_address(bus_number)  # Get I2C device address
    i2c_bus = SMBus(bus_number)  # Open I2C bus
    bmp = Bmp280(i2c_bus, address)

    delay = 60 / samplespm
    while True:
        start_time = time.time()  # Start time tracking
        
        sum_temperature1 = 0
        sum_temperature2 = 0
        
        for _ in range(samplespm):
            sum_temperature1 += bmp._read_temperature()
            sum_temperature2 += device_temperature.read_cpu_temperature()
            time.sleep(delay)
        
        elapsed_time = time.time() - start_time  # Total loop time
        print(f"Loop execution time: {elapsed_time:.2f} seconds")

        average_temp_i2c = sum_temperature1 / samplespm
        average_temp_raspi = sum_temperature2 / samplespm

        print(f"Average I2C CPU Temp = {average_temp_i2c:.2f}°C")
        print(f"Average Raspberry Pi CPU Temp = {average_temp_raspi:.2f}°C")

        # Adjust the sleep time so that total duration is as close to 60s as possible
        remaining_time = 60 - elapsed_time
        if remaining_time > 0:
            time.sleep(remaining_time)
