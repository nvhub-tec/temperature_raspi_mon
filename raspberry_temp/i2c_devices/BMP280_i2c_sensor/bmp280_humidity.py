from smbus2 import SMBus
from i2c_devices.BMP280_i2c_sensor.bmp280_temperature import Bmp280

class Bmp280Humidity:

    """initializes relevant humidity registers, reads raw data, writes to register,
    converts data
    """

    def __init__(
            self,
            i2c_bus: SMBus,
            i2c_device_address: int,
            bmp_sensor: Bmp280
            ):
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_device_address
        self.bmp_sensor = bmp_sensor

        self.dig_h1 = int.from_bytes(self.i2c_read_hum_block(0xA1, 1),
                                     byteorder = 'little', signed = False)
        self.dig_h2 = int.from_bytes(self.i2c_read_hum_block(0xE1, 2),
                                     byteorder = 'little', signed = True)
        self.dig_h3 = int.from_bytes(self.i2c_read_hum_block(0xE3, 1),
                                     byteorder = 'little', signed = False)
        self.dig_h4 = int.from_bytes(self.i2c_read_hum_block(0xE4, 2),
                                     byteorder = 'little', signed = True)
        self.dig_h5 = int.from_bytes(self.i2c_read_hum_block(0xE5, 2),
                                     byteorder = 'little', signed = True)
        self.dig_h6 = int.from_bytes(self.i2c_read_hum_block(0xE7, 1),
                                     byteorder = 'little', signed = True)

        self.i2c_write_hum_block(0xF2, 1)

        self.temp_for_humidity = bmp_sensor.get_temp_for_humidity

    def i2c_read_hum_block(self, register: int, length: int) -> list[int]:
        """reads data from a specified register

        Args:
            register (int): register address to read
            length (int): number of bytes to read
        """

        return self.i2c_bus.read_i2c_block_data(
            self.i2c_address,
            register,
            length
        )

    def i2c_write_hum_block(self, register:int, length: int):
        """
    Writes data to a specified I2C register.

    Args:
        register (int): The register address to write to.
        length (int): number of bytes to write
    """
    
        return self.i2c_bus.write_byte_data(
            self.i2c_address,
            register,
            length
        )

    def raw_humid_data(self) -> tuple:
        """reads raw humid data

        Returns:
            tuple: lists the register and number of them to read,
            returns first item in each tuple
        """
        raw_humid1 = self.i2c_read_hum_block(0xFD, 1)[0]
        raw_humid2 = self.i2c_read_hum_block(0xFE, 1)[0]
        return raw_humid1, raw_humid2

    def read_humidity(self) -> int:
        """converts to Relative Humidity using bit-shifts 
        Returns: %RH value
        """

        raw_humid1, raw_humid2 = self.raw_humid_data()
        adc_h = (raw_humid1 << 8) | raw_humid2


        humidity = (adc_h / 65536.0) * 100.0
        return humidity
    