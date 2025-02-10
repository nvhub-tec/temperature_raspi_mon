from time import sleep
import os
from smbus2 import SMBus
from get_bus_and_address import find_i2c_bus, find_i2c_address

class Bmp280:
    
    """_summary_
    """
    def __init__(self):
    
        self.i2c_bus = SMBus(find_i2c_bus)
        self.i2c_address = find_i2c_address(self.i2c_bus)
        
        #registers to read from
        self.dig_T1 = self._i2c_read_block(0x88, 2)
        self.dig_T2 = self._i2c_read_block(0x8A, 2)
        self.dig_T3 = self._i2c_read_block(0x8C, 2)
        
        if (self.dig_T2 > 32767): 
            self.dig_T2 -= 65536
        if (self.dig_T3 > 32767):
            self.dig_T3 -= 65536
        
        #registers to write to 
        self._i2c_write_byte(0xf5, (5<<5))
        self._i2c_write_byte(0xf4, (5<<5))
        

        
    def _i2c_read_block(self, register: int, length: int) -> list[int]:
  
        return self.i2c_bus.read_i2c_block_data(
            self.i2c_address,
            register,
            length
        )
        
    def _i2c_write_byte(self, register: int, value: int):
        return self.i2c_bus.write_byte_data(
            self.i2c_address,
            register,
            value
        )

    def read_raw_temperature(self) -> tuple:
        d1 = self._i2c_read_block(0xfa, 1)[0]
        d2 = self._i2c_read_block(0xfb, 1)[0]
        d3 = self._i2c_read_block(0xfc, 1)[0]
        return d1, d2, d3
        
    def _read_temperature(self) -> float:
        
        d1, d2, d3 = self.read_raw_temperature()
        
        adc_T  = ((d1 << 16) | (d2 << 8) | d3) >> 4

        var1 = ((((adc_T>>3) - (self.dig_T1<<1))) * (self.dig_T2)) >> 11
        var2 = (((((adc_T>>4) - (self.dig_T1)) * ((adc_T>>4) - (self.dig_T1))) >>12) * (self.dig_T3)) >> 1
        t_fine = var1 +var2
        T = (t_fine * 5 +128) >> 8
        T = T / 100

        return T
    

   