import subprocess

def normal_mode_on(): 
    
    i2c_forced_mode = ["i2cset", "-y", i2c_bus, address, "0xf4", "0x01"]
    subprocess.check_output(i2c_forced_mode)