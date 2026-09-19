import statistics 
from statistics import mean, median 
import random 
import sys
from datetime import datetime, date, time, timedelta

def main():

    now = datetime.now()
    total_readings = 0

    demo_lenth = len(sys.argv)
    
    if demo_lenth > 1:
        if sys.argv[1] =="demo":
            temp_readings_list = [random.randint(1, 200) for _ in range(10)]
            total_num_readings = 10
        else:
            temp_readings_list = get_readings()    
    else:    
       temp_readings_list = get_readings()

    for i in temp_readings_list:
        total_readings += i   

    total_num_readings = len(temp_readings_list)
    averages = average(temp_readings_list)
    extreme = extremes(temp_readings_list)
    classific = count_by_class(temp_readings_list)
    out_range_readings = flag_anomalies (temp_readings_list, total_readings, total_num_readings)

    print(f"Total Number of Readings: {total_num_readings}\n Total Readings {total_readings}\n Mean: {averages[0]:.1f}\n Median: {averages[1]}\n Minimum: {extreme[0]}\n Maximum: {extreme[1]}")
    print(f"count_by_classification: {classific}")
    print(f"Out Of Range Readings: {out_range_readings}\n DateTime: {now}")
    

    report_to_file(averages, extreme, classific, total_num_readings, total_readings, out_range_readings )

    sys.exit(0)

def get_reading():

    status = True 
    
    while True:
        try:
            temp_reading = float(input("Enter the temperature reading: "))
            break

        except ValueError:
            print(f"Enter an integer!!!")

        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Goodbye!")
            sys.exit(0)    

  
    while status == True:
        try:
            Unit = str(input("Enter the unit C or F: "))

        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Goodbye!")
            sys.exit(0) 

        unit = Unit.lower()

        if unit != "c" and unit != "f" : 
            print("Wrong unit: ")
            
            status = True
        else: 
            status = False    
            
    if unit == "f":
        temp_reading =  (temp_reading - 32) *5/9

    return temp_reading    

def average(readings):
    mean_temp = statistics.mean(readings)
    median_temp = statistics.median(readings)
    return mean_temp , median_temp

def extremes(readings):

    high = 0
    for p in range(len(readings)-1):
        for i in range(len(readings)-1):
            if readings[i] >= readings[i +1]:
                high = readings[i]
                readings[i] = readings[i+1] 
                readings[i+1] = high 

    minimum = readings[0]
    maximum = readings[len(readings)-1]

    return minimum , maximum 
   
def classify(reading):
    if reading < 18:
        return "low"
    if reading >= 18 and reading <=30:
        return "normal"
    if reading > 30:
        return "high"        

def count_by_class(readings):
    classification_dict = {}
    
    for value in readings:
        category = classify (value) 
        if category in classification_dict:
            classification_dict[category].append(value)
        else:    
            classification_dict[category] = [value] 
       
    return  classification_dict    
  

def report_to_file(avg, extrm, cbc, tot_num_rdgs, tot_rdgs, out_range_rdgs ):
    now = datetime.now()
    with open("temp_readings.txt", "w", encoding="utf-8") as file:
        file.write(f" Total Number of Readings: {tot_num_rdgs}\n Total Readings {tot_rdgs}\n Mean: {avg[0]}\n Median: {avg[1]}\n Minimum: {extrm[0]}\n Maximum: {extrm[1]}\n")
        file.write(f"Out Of Range Readings: {out_range_rdgs}\n")
        file.write(f"count_by_classification: {cbc}\n")
        file.write(f"DateTime: {now}")


def flag_anomalies (readings, tot_rdgs, tot_num_rdgs):
    avg = tot_rdgs / tot_num_rdgs

    out_range_reading = []
    for reading in readings:
        if reading > (avg + 10) or reading < (avg - 10):
            out_range_reading.append(reading)

    return out_range_reading

def get_readings():

    temp_readings_lt = []
        
    while True:
        reading = get_reading()
        
        temp_readings_lt.append(reading)

        total_num_readings = len(temp_readings_lt)
        if total_num_readings >= 3:
            try:
                Decision = str(input("Do you want to continue or stop? Enter done / cont: "))
                decision = Decision.lower()

            except ValueError:
                print(" Wrong decision!! kindlly enter done or cont to stop or continue respectively")

            if decision == "done":
                break

    return temp_readings_lt       

    

if __name__ == "__main__":
    main()