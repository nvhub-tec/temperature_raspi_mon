import smbus
from time import sleep

bmp280_id = 0x76
i2c = smbus.SMBus(1)

i2c.write_byte_data(bmp280_id, 0xf5, (5<<5))
i2c.write_byte_data(bmp280_id, 0xf4, (5<<5))

dig_T1 = i2c.read_word_data(bmp280_id, 0x88)
dig_T2 = i2c.read_word_data(bmp280_id, 0x8A)
dig_T3 = i2c.read_word_data(bmp280_id, 0x8C)

if (dig_T2 > 32767):
    dig_T2 -= 65536
if (dig_T3 > 32767):
    dig_T3 -= 65536
    
while True:
    d1 = i2c.read_byte_data(bmp280_id, 0xfa)
    d2 = i2c.read_byte_data(bmp280_id, 0xfb)
    d3 = i2c.read_byte_data(bmp280_id, 0xfc)

    adc_T  = ((d1 << 16) | (d2 << 8) | d3) >> 4

    var1 = ((((adc_T>>3) - (dig_T1<<1))) * (dig_T2)) >> 11;
    var2 = (((((adc_T>>4) - (dig_T1)) * ((adc_T>>4) - (dig_T1))) >>12) * (dig_T3)) >> 14;
    t_fine = var1 +var2;
    T = (t_fine * 5 +128) >> 8;
    T = T / 100

    print("Temperature: " +str(T))
    sleep(1)