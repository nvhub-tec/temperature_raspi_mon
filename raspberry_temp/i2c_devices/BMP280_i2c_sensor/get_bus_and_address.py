import os
from time import sleep
from smbus2 import SMBus


def find_i2c_bus():
    
    """
    checks directory for devices beginning with i2c-,
    returns first available bus number
    """
        
    busses = [int(dev[-1]) for dev in os.listdir('/dev') if dev.startswith ('i2c-')]
    if not busses:
        raise RuntimeError("No device found at this address on any bus")
    return busses[0]


def find_i2c_address(i2c_bus: int = None) -> int: # method to identify address
    
    """
    accesses bus, iterates through list, 
    """
    
    if i2c_bus is None:
        i2c_bus = find_i2c_bus()

    bus = SMBus(i2c_bus)

    for address in range (120):
        try:
            bus.read_byte(address)
            return(address)
        except IOError:
            continue
    bus.close()
    raise RuntimeError(f"No address found on bus {bus}")