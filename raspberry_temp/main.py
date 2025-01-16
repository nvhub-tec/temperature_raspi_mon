import time

class device_temp:
    def __init__ (self, samplerate, cpu_temp_path, gpu_temp, store_cpu_temp, store_gpu_temp):
        self.samplerate = sample_rate
        self.cpu_temp_path = "//sys//class//thermal//thermal_zone0//temp"
        self.gpu_temp = "vcgencmd measure_temp" #terminal command
        self.store_cpu_temp = []
        self.store_gpu_temp = []
    

    def read_gpu_temp(self):    #shell command, convert from byte str, format, handle errors
        try:
            output = subprocess.check_output("vcgencmd"/ "measure_temp").decode("utf-8")
            gpu_temp = output.split("=")[1].split("'")[0]
            return round(float(gpu_temp)) 
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
        # cpu_temp = read_temp_file()
        # print(f"cpu temperature, degrees Celcius: ", {cpu_temp})
        
        
        
def sampling_method(self):
    cpuTempSample = read_temp_file
    gpuTempSample = read_gpu_temp
    
    if cpuTempSample is not None:
        print(f"CPU temperature: {cpuTempSample:.2f}°C")
        
    if gpuTempSample is not None:
        print(f"GPU temperature: {gpuTempSample:.2f}°C")
            
            
            
def sample_rate(self):
    sampleRate = input(int(10))
    next_sample = time.time()

while True:
    sample_rate()
    read_temp_file()
    #read_gpu_file
    
next_sample += sampleRate
remaining_time = next_sample - time.time()
if remaining_time > 0:
    time.sleep(remaining_time)