from smbus2 import SMBus
from raspi_temperature_driver.averaging_raspi_temperature import average_temp_per_minute

def main():
    """main function, edit bus number and address here.
    calls on the function that times readings for temp
    and humidity, passing in these values
    """

    bus_number = 1               # find_i2c_bus()  #  Find the I2C bus
    address = 0x76               # find_i2c_address(bus_number)  #  Find the I2C address
    i2c_bus = SMBus(bus_number)  # open bus

    average_temp_per_minute(device_temperature=None, i2c_bus=i2c_bus, address=address)


if __name__ == '__main__':
    main()
