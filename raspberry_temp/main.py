import time
from sys_requirements import check_system_requirements
from temperature_class import device_temperature

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