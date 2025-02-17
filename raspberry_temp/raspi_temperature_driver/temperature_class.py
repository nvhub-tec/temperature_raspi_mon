class DeviceTemperature:
    """Reads CPU temperature from the Raspberry Pi's thermal zone file."""
    
    def __init__(self, cpu_thermal_zone_path: str = "/sys/class/thermal/thermal_zone0/temp"):
        self.cpu_thermal_zone_path = cpu_thermal_zone_path
    
    def read_cpu_temperature(self) -> float:
        """Reads and returns the CPU temperature in Celsius."""
        with open(self.cpu_thermal_zone_path, encoding="utf-8") as file:
            cpu_temperature = file.read()
            return int(cpu_temperature) / 1000.0
  