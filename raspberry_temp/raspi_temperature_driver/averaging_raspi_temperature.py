import time
from smbus2 import SMBus
from i2c_devices.BMP280_i2c_sensor.bmp280 import Bmp280
from i2c_devices.BMP280_i2c_sensor.get_bus_and_address import find_i2c_bus, find_i2c_address


def average_temp_per_minute():
    """
    main function, timing when to sample temperature based on input,
    averaging, printing and error handling
    """
    
    try:
        samplespm = int(input("Input samples per minute: "))
        if samplespm <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
        return
    
    # Initialize BMP280 sensor
    bus_number = find_i2c_bus()  # Get I2C bus number
    address = find_i2c_address(bus_number)  # Get I2C device address
    i2c_bus = SMBus(bus_number)  # Open I2C bus
    bmp = Bmp280(i2c_bus, address)
    
    try: 
        delay = 60 / samplespm
        while True:
            count = 0
            sum_temperature = 0
         
            while count <= samplespm:
    
                sum_temperature += bmp._read_temperature()
             
                count+=1
                time.sleep(delay)
      
            average_temp = sum_temperature/ samplespm
            print(f"average cpu temp = {average_temp:.2f}°C")
            
    except ValueError:
        ("Invalid input, enter a positive integer.")