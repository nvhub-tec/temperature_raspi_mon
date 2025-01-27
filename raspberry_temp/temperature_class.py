import subprocess

class device_temperature:
    def __init__ (self, cpu_temperature, gpu_temperature):
    
        self.cpu_temperature = cpu_temperature  #"//sys//class//thermal//thermal_zone0//temp"
        self.gpu_temperature = gpu_temperature  #"vcgencmd measure_temp" #terminal command

    
    def read_gpu_temperature(self): #shell command, convert from byte str, format, handle errors
        try:
            output = subprocess.check_output(["//usr//bin//vcgencmd", "measure_temp"]).decode("utf-8")
            gpu_temp = output.split("=")[1].split("'")[0]
            
            return float(gpu_temp)
        except FileNotFoundError:
            raise Exception("Failed to read GPU temperature: 'vcgencmd' command not found. Ensure it is installed.")
        except ValueError:
            
            raise Exception("Failed to read GPU temperature: Output from 'vcgencmd' is not a valid number.")
        except subprocess.CalledProcessError as e:
        
            raise Exception(f"Failed to read GPU temperature: 'vcgencmd' command failed with error: {e}")
        except Exception as e:
        
            raise Exception(f"Failed to read GPU temperature: {e}")
    

    def read_cpu_temperature(self):
        with open("//sys//class//thermal//thermal_zone0//temp", "r") as file:
            cpu_temp = file.read()
            return int(cpu_temp) / 1000.0