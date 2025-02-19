from dataclasses import dataclass
import time
from smbus2 import SMBus
from i2c_devices.BMP280_i2c_sensor.get_bus_and_address import find_i2c_bus, find_i2c_address


@dataclass
class Bmp280Config:
    inactivity_duration: int = 0
    iir_filter: int = 0
    spi_enable: int = 0

def config_value(config: Bmp280Config) -> int:
    """Converts configuration settings into a single integer."""
    return (config.inactivity_duration << 5 |
            config.iir_filter << 2 |
            config.spi_enable)
    
    
class Bmp280:
    
    """_summary_
    """
    def __init__(
        self,
        i2c_bus: SMBus,
        i2c_device_address: int
    ):
        self._i2c_bus = i2c_bus
        self._i2c_address = i2c_device_address
        
        #registers to read from
        self.dig_T1 = int.from_bytes(self._i2c_read_block(0x88, 2), byteorder="little", signed=False)
        self.dig_T2 = int.from_bytes(self._i2c_read_block(0x8A, 2), byteorder="little", signed=True)
        self.dig_T3 = int.from_bytes(self._i2c_read_block(0x8C, 2), byteorder="little", signed=True)
        
        
        #registers to write to 
        self._i2c_write_byte(0xf5, (5<<5))
        self._i2c_write_byte(0xf4, (5<<5))
        
        config = Bmp280Config()
        config.iir_filter = 4
        
    def _i2c_read_block(self, register: int, length: int) -> list[int]:
  
        return self._i2c_bus.read_i2c_block_data(
            self._i2c_address,
            register,
            length
        )
        
    def _i2c_write_byte(self, register: int, value: int):
        return self._i2c_bus.write_byte_data(
            self._i2c_address,
            register,
            value
        )
        
    def _i2c_write_block(self, register: int, values: list[int]) -> None:
        """Writes a list of values to the specified I2C register."""
        self._i2c_bus.write_i2c_block_data(self._i2c_address, register, values)
        
    def reset_configure_mode(self):
        
        self._i2c_write_block(0xB6, [0XE0])
        time.sleep(0.1)
        
        config = Bmp280Config(inactivity_duration=5, iir_filter=4, spi_enable=0)
        config_value_int = config_value(config)
        self._i2c_write_block(0xF5, [config_value_int])
        
        self._i2c_write_byte(0xF4, 0x27)
        
    def read_raw_temperature(self) -> tuple:
        
        d1 = self._i2c_read_block(0xfa, 1)[0]
        d2 = self._i2c_read_block(0xfb, 1)[0]
        d3 = self._i2c_read_block(0xfc, 1)[0]

        return d1, d2, d3
        
    def read_temperature(self) -> float:
        
        self.reset_configure_mode()  # Make sure the sensor is in forced mode

        time.sleep(0.1)
        
        d1, d2, d3 = self.read_raw_temperature()
        
        adc_T  = ((d1 << 16) | (d2 << 8) | d3) >> 4
    
    # Calculate var1
        var1 = (adc_T / 16384.0 - self.dig_T1 / 1024.0) * self.dig_T2
        
        # Calculate var2
        var2 = (adc_T / 131072.0 - self.dig_T1 / 8192.0) * (adc_T / 131072.0 - self.dig_T1 / 8192.0) * self.dig_T3
        
        # Calculate temperature
        temp = (var1 + var2) / 5120.0
        
        return temp