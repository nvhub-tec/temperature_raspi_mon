import time
import subprocess
from smbus2 import SMBus
from i2c_devices.BMP280_i2c_sensor.bmp280 import Bmp280
from i2c_devices.BMP280_i2c_sensor.get_bus_and_address import find_i2c_bus, find_i2c_address


def main():

    # bus_number = 1               # find_i2c_bus()  #  Find the I2C bus
    # address = 0x76               # find_i2c_address(bus_number)  #  Find the I2C address
    # i2c_bus = SMBus(bus_number)  # open bus

    # bmp = Bmp280(
    #     i2c_bus,
    #     address
    # )

    # average_temp_per_minute()
    
    bus_number = find_i2c_bus()
    address = find_i2c_address(bus_number)
    i2c_bus = SMBus(bus_number)

    bmp = Bmp280(i2c_bus, address)

    while True:
        temp = bmp._read_temperature()
        print(f"Temperature: {temp:.2f}°C")
        time.sleep(15)  # Wait before taking another reading

if __name__ == '__main__':
    main()
