import subprocess

class device_temperature:
    """
    gpu and cpu temperature sampling methods with error handling
    """
    
    def __init__ (
        self,
        cpu_thermal_zone_path: str = "//sys//class//thermal//thermal_zone0//temp", 
        
    ):
        self.cpu_thermal_zone_path = cpu_thermal_zone_path


    def read_cpu_temperature(self):
        with open(self.cpu_thermal_zone_path, "r") as file:
            cpu_temperature = file.read()
            return int(cpu_temperature) / 1000.0