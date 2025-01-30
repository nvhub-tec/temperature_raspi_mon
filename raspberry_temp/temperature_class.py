import subprocess

class device_temperature:
    """
    gpu and cpu temperature sampling methods with error handling
    """
    
    def __init__ (
        self,
        cpu_thermal_zone_path: str = "//sys//class//thermal//thermal_zone0//temp", 
        gpu_thermal_zone_path: str = "usr//bin//vcgencmd measure_temp"
    ):
        self.cpu_thermal_zone_path = cpu_thermal_zone_path
        self.gpu_thermal_zone_path = gpu_thermal_zone_path

    
#    def read_gpu_temperature(self): 
        """
        shell command, convert from byte str, format, handle errors
        - broken vcgencmd
        """
#        try:
#            output = subprocess.check_output([self.gpu_thermal_zone_path]).decode("utf-8")
#            gpu_temperature = output.split("=")[1].split("'")[0]
#            
#            return float(gpu_temperature)
#        except FileNotFoundError:
#            raise Exception(
#                "Failed to read GPU temperature:'vcgencmd' command not found."
#            )
#        except ValueError:  
#            raise Exception(
#                "Failed to read GPU temperature: "
#                "Output from 'vcgencmd' is not a valid number."
#                            )
#        except subprocess.CalledProcessError as e:
#            raise Exception(
#                f"Failed to read GPU temperature:"
#                "'vcgencmd' command failed with error: {e}"
#                )
#        except Exception as e:
#            raise Exception(f"Failed to read GPU temperature: {e}")

    def read_cpu_temperature(self):
    """
    opens the file containing current cpu temperature
    """    
        with open(self.cpu_thermal_zone_path, "r") as file:
            cpu_temperature = file.read()
            return int(cpu_temperature) / 1000.0