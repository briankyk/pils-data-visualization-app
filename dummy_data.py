# Data to be generated :
# DATE, TIME, NUMBER_OF_SEC_SINCE_THE_START, TIP_TEMP, STEAM_HEATER_TEMP
import random
import datetime

#file = open("dat_1.dat", "w+")
#file = open("dat_2.dat", "w+")
file = open("dat_3.dat", "w+")

today = datetime.date.today()
today = today.strftime("%d/%m/%Y")
time_now = datetime.datetime.now()
time_now = time_now.strftime("%H:%M:%S")

for i in range(1):
    file.write("header" + "\n")
    print("header")
    # pass

for i in range(2, 1002):
    rand_data = [today,  time_now, i-1,
                 # random.randint(95, 105), random.randint(95, 105)]
                 # random.randint(80, 100), random.randint(80, 100)]
                 random.randint(100, 120), random.randint(100, 120)]
    rand_data_str = str(rand_data)
    rand_data_str = rand_data_str[1:-1]
    file.write(rand_data_str + "\n")
    print(rand_data_str)
