from smbus2 import SMBus

class Bmp280_humidity:
   
    """_summary_
    """

    def __init__(
            self,
            i2c_bus: SMBus,
            i2c_device_address: int
    ):
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_device_address
            
        self.dig_H1 = int.from_bytes(self.i2c_read_hum_block(0xA1, 1),byteorder = 'little', signed = False)
        self.dig_H2 = int.from_bytes(self.i2c_read_hum_block(0xE1, 2),byteorder = 'little', signed = True)
        self.dig_H3 = int.from_bytes(self.i2c_read_hum_block(0xE3, 1),byteorder = 'little', signed = False)
        self.dig_H4 = int.from_bytes(self.i2c_read_hum_block(0xE4, 2),byteorder = 'little', signed = True)
        self.dig_H5 = int.from_bytes(self.i2c_read_hum_block(0xE5, 2),byteorder = 'little', signed = True)
        self.dig_H6 = int.from_bytes(self.i2c_read_hum_block(0xE7, 1),byteorder = 'little', signed = True)
        
        self.i2c_write_hum_block(0xF2, 1)
        
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
        raw_humid1 = self.i2c_read_hum_block(0xFE, 1)[0]
        raw_humid2 = self.i2c_read_hum_block(0xFD, 1)[0]
        return raw_humid1, raw_humid2
        
    def compensate_humidity(self, adc_H: float,t_fine: float) -> float:
        
        raw_humid1, raw_humid2 = self.raw_humid_data()
        adc_H = (raw_humid1 << 8) | raw_humid2

        
        var_H = t_fine - 76800.0
        var_H = (adc_H - (self.dig_H4 * 64.0 + (self.dig_H5 / 16384.0) * var_H)) * (
            (self.dig_H2 / 65536.0) * (1.0 + (self.dig_H6 / 67108864.0) * var_H *
            (1.0 + (self.dig_H3 / 67108864.0) * var_H)))
        
        var_H = var_H * (1.0 - (self.dig_H1 * var_H / 524288.0))

        if var_H > 100.0:
            var_H = 100.0
        elif var_H < 0.0:
            var_H = 0.0
            
        return var_H