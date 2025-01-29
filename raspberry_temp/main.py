import time

from sys_requirements import check_system_requirements
from temperature_class import device_temperature

check_system_requirements()

try:
    samplespm = int(input("Input samples per minute: "))
except ValueError:
    print("Invalid input. Please enter a positive integer.")
    SystemExit(1)     

camera1 = device_temperature("//sys//class//thermal//thermal_zone0//temp",
                             "vcgencmd measure_temp") 
 
"""creating the object, give it the class attributes"""


def main():
    """main function, timing when to sample temperature,
    averaging, printing and error handling"""
    
    try:
        
        delay = 60 / samplespm
        while True:
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
       

if __name__ == '__main__':
    main()
      