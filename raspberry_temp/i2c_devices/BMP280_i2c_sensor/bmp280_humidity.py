from smbus2 import SMBus
from i2c_devices.BMP280_i2c_sensor.bmp280_temperature import Bmp280

class Bmp280_humidity:
   
    """_summary_
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

        self.dig_H1 = int.from_bytes(self.i2c_read_hum_block(0xA1, 1),byteorder = 'little', signed = False)
        self.dig_H2 = int.from_bytes(self.i2c_read_hum_block(0xE1, 2),byteorder = 'little', signed = True)
        self.dig_H3 = int.from_bytes(self.i2c_read_hum_block(0xE3, 1),byteorder = 'little', signed = False)
        self.dig_H4 = int.from_bytes(self.i2c_read_hum_block(0xE4, 2),byteorder = 'little', signed = True)
        self.dig_H5 = int.from_bytes(self.i2c_read_hum_block(0xE5, 2),byteorder = 'little', signed = True)
        self.dig_H6 = int.from_bytes(self.i2c_read_hum_block(0xE7, 1),byteorder = 'little', signed = True)

        self.i2c_write_hum_block(0xF2, 1)

        self.temp_for_humidity = bmp_sensor.get_temp_for_humidity

    def i2c_read_hum_block(self, register: int, length: int) -> list[int]:

        return self.i2c_bus.read_i2c_block_data(
            self.i2c_address,
            register,
            length
        )

    def i2c_write_hum_block(self, register:int, length: int):

        return self.i2c_bus.write_byte_data(
            self.i2c_address,
            register,
            length
        )

    def raw_humid_data(self) -> tuple:
        raw_humid1 = self.i2c_read_hum_block(0xFD, 1)[0]
        raw_humid2 = self.i2c_read_hum_block(0xFE, 1)[0]
        return raw_humid1, raw_humid2

    def read_humidity(self):

        temp_for_rh = self.bmp_sensor.get_temp_for_humidity()
        raw_humid1, raw_humid2 = self.raw_humid_data()
        adc_H = (raw_humid1 << 8) | raw_humid2


        humidity = (adc_H / 65536.0) * 100.0
        return humidity