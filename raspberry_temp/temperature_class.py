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
            print("Error: vcgencmd not found: ensure it is installed")
            return None
        except Exception as e:
            print(f"Error reading gpu temperature {e}")
            return None
    

    def read_cpu_temperature(self):
        with open("//sys//class//thermal//thermal_zone0//temp", "r") as file:
            cpu_temp = file.read()
            return int(cpu_temp) / 1000.0