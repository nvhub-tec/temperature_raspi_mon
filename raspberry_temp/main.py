from smbus2 import SMBus
from raspi_temperature_driver.averaging_raspi_temperature import average_temp_per_minute

def main():
    """main function, edit bus number and address here.
    calls on the function that times readings for temp
    and humidity, passing in these values
    """

    bus_number = 1               # i2c device bus
    address = 0x76               # i2c device address
    i2c_bus = SMBus(bus_number)  # open bus

    average_temp_per_minute(device_temperature=None, i2c_bus=i2c_bus, address=address)


if __name__ == '__main__':
    main()
