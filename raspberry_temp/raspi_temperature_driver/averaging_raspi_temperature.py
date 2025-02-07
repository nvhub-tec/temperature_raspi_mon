import time

from sys_requirements import check_system_requirements
from temperature_class import device_temperature


def average_temp_per_minute():
    """
    main function, timing when to sample temperature based on input,
    averaging, printing and error handling
    """
    
    try:
        samplespm = int(input("Input samples per minute: "))
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
    SystemExit(1)
    
    check_system_requirements()
    camera1 = device_temperature()
    
    try: 
        delay = 60 / samplespm
        while True:
            count = 0
            sum_temperature = 0
         
            while count <= samplespm:
    
                sum_temperature += camera1.read_cpu_temperature()  
             
                count+=1
                time.sleep(delay)
      
            average_temp = sum_temperature/ samplespm
            print(f"average cpu temp = {average_temp:.2f}°C")
            
    except ValueError:
        ("Invalid input, enter a positive integer.")