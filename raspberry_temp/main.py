import time
import subprocess
import platform
import sys


def check_system_requirements():
    # Check if running on Linux
    if platform.system() != "Linux":
        print("Error: This script is designed to run on Linux")
        sys.exit(1)
        
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
        
        

camera1 = device_temperature("//sys//class//thermal//thermal_zone0//temp", "vcgencmd measure_temp")  #creating the object

        #initialise loop count, variable to sum all temperatures
samplespm = int(input("input samples per minute: "))

def main():
    try:
        
    
        delay = 60 / samplespm
        count = 0
        sum_temperature = 0
        sum_temperature2 = 0
        while count <= samplespm:
    
            sum_temperature += camera1.read_cpu_temperature()  #use cpu temp method, add to variable
            sum_temperature2 += camera1.read_gpu_temperature()
            count+=1
            time.sleep(delay)
      
        average_temp = sum_temperature/ samplespm
        print(f"average cpu temp = {average_temp:.2f}°C")
        average_temp2 = sum_temperature2/ samplespm
        print(f"average gpu temp = {average_temp2:.2f}°C")
    except ValueError:
        ("Invalid input, enter a positive integer.")
       
        
a = 1
while True:
    main()