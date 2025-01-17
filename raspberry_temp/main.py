import time

import subprocess


class device_temp:
    def __init__ (self, cpu_temp_path, gpu_temp):
    
        self.cpu_temp_path = cpu_temp_path  #"//sys//class//thermal//thermal_zone0//temp"
        self.gpu_temp = gpu_temp  #"vcgencmd measure_temp" #terminal command

    

    def read_gpu_temp(self):    #shell command, convert from byte str, format, handle errors
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
    


    def read_temp_file(self):
        with open("//sys//class//thermal//thermal_zone0//temp", "r") as file:
            temp_str = file.read()
            return int(temp_str) / 1000.0
        
        

camera1 = device_temp("//sys//class//thermal//thermal_zone0//temp", "vcgencmd measure_temp")  #creating the object

        #initialise loop count, variable to sum all temperatures
samplespm = int(input("input samples per minute: "))
def averaging_values():
    try:
        
    
        delay = 60 / samplespm
        count = 0
        sum_temperature = 0
        sum_temperature2 = 0
        while count <= samplespm:
    
            sum_temperature += camera1.read_temp_file()  #use cpu temp method, add to variable
            sum_temperature2 += camera1.read_gpu_temp()
            count+=1
            time.sleep(1)
      
        average_temp = sum_temperature/ samplespm
        print(f"average cpu temp = {average_temp:.2f}°C")
        average_temp2 = sum_temperature2/ samplespm
        print(f"average gpu temp = {average_temp2:.2f}°C")
    except ValueError:
        ("Invalid input, enter a positive integer.")
       
        
a = 1
while True:
    averaging_values()
        
        
        
