
def read_temp_file():
    with open(r"//sys//class//thermal//thermal_zone0//temp", "r") as file:
                    temp_str = file.read() 
                    return int(temp_str) / 1000.0
                
cpu_temp = read_temp_file
print(f"cpu temperature, degrees Celcius: ", {cpu_temp})
            