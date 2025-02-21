from smbus2 import SMBus
from i2c_devices.BMP280_i2c_sensor.bmp280_temperature import Bmp280
from i2c_devices.BMP280_i2c_sensor.bmp280_humidity import Bmp280_humidity
from raspi_temperature_driver.averaging_raspi_temperature import average_temp_per_minute

def main():

    bus_number = 1               # find_i2c_bus()  #  Find the I2C bus
    address = 0x76               # find_i2c_address(bus_number)  #  Find the I2C address
    i2c_bus = SMBus(bus_number)  # open bus

    bmp = Bmp280(
        i2c_bus,
        address
    )

    humidity_sensor = Bmp280_humidity(i2c_bus, address, bmp)
    
    average_temp_per_minute()

if __name__ == '__main__':
    main()
