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
        
        self.dig_h1 = int.from_bytes(self.i2c_read_block(0xA1, 1),byteorder = 'little', signed = False)
        self.dig_h2 = int.from_bytes(self.i2c_read_block(0xE1, 2),byteorder = 'little', signed = True)
        self.dig_h3 = int.from_bytes(self.i2c_read_block(0xE3, 1),byteorder = 'little', signed = False)
        self.dig_h4 = int.from_bytes(self.i2c_read_block(0xE4, 2),byteorder = 'little', signed = True)
        self.dig_h5 = int.from_bytes(self.i2c_read_block(0xE5, 2),byteorder = 'little', signed = True)