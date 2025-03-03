from dataclasses import dataclass
import time
from smbus2 import SMBus


@dataclass
class Bmp280Config:
    """configuration settings for the bmp280
    """
    inactivity_duration: int = 0
    iir_filter: int = 0
    spi_enable: int = 0

def config_value(config: Bmp280Config) -> int:
    """Converts configuration settings into a single integer."""
    return (config.inactivity_duration << 5 |
            config.iir_filter << 2 |
            config.spi_enable)


class Bmp280:

    """retrieves bus number and address, initializes relevant temp registers.
    resets normal mode for every read, reads raw register data and converts it,
    allows for temp to be passed to the humidity class
    """
    def __init__(
        self,
        i2c_bus: SMBus,
        i2c_device_address: int
    ):
        self._i2c_bus = i2c_bus
        self._i2c_address = i2c_device_address
        self.t_fine = 0

        #registers to read from
        self.dig_t1 = int.from_bytes(self._i2c_read_block(0x88, 2),
                                     byteorder="little", signed=False)
        self.dig_t2 = int.from_bytes(self._i2c_read_block(0x8A, 2),
                                     byteorder="little", signed=True)
        self.dig_t3 = int.from_bytes(self._i2c_read_block(0x8C, 2),
                                     byteorder="little", signed=True)

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
        """resets the device,sets the config
        and sets to normal -
        to be used when timing each reading
        """

        self._i2c_write_block(0xB6, [0XE0])
        time.sleep(0.1)

        config = Bmp280Config(inactivity_duration=5, iir_filter=4, spi_enable=0)
        config_value_int = config_value(config)
        self._i2c_write_block(0xF5, [config_value_int])

        self._i2c_write_byte(0xF4, 0x27)
        self._i2c_write_byte(0xF2, 0x01)

    def read_raw_temperature(self) -> tuple:

        """returns raw values from the specified registers
        """

        d1 = self._i2c_read_block(0xfa, 1)[0]
        d2 = self._i2c_read_block(0xfb, 1)[0]
        d3 = self._i2c_read_block(0xfc, 1)[0]

        return d1, d2, d3

    def read_temperature(self) -> float:
        """uses raw values to calculate value in °C

        Returns:
            float: _description_
        """

        self.reset_configure_mode()  # Make sure the sensor is in forced mode

        time.sleep(0.1)

        d1, d2, d3 = self.read_raw_temperature()

        adc_t  = ((d1 << 16) | (d2 << 8) | d3) >> 4

    # Calculate var1
        var1 = (adc_t / 16384.0 - self.dig_t1 / 1024.0) * self.dig_t2

        var2 = (adc_t / 131072.0 - self.dig_t1 / 8192.0) * (adc_t / 131072.0 - self.dig_t1 / 8192.0) * self.dig_t3

        self.t_fine = var1 + var2
        temp = self.t_fine / 5120.0

        return temp

    def get_temp_for_humidity(self) -> float:
        """saves the temperature value for the humidity calculation
        Returns:
            float: temperature
        """
        self.read_temperature()

        return self.t_fine
    