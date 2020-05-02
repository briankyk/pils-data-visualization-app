# Data to be generated :
# DATE, TIME, NUMBER_OF_SEC_SINCE_THE_START, TIP_TEMP, STEAM_HEATER_TEMP
import os
import random
import time
import datetime

file = open("dat_cont.dat", "w+")

for i in range(1):
    file.write("header" + "\n")
    print("header")
    # pass

for i in range(2, 3602):

    today = datetime.date.today()
    today = today.strftime("%d/%m/%Y")
    time_now = datetime.datetime.now()
    time_now = time.strftime("%H:%M:%S")
    rand_data = [today,  time_now, i-1,
                 random.randint(90, 110), random.randint(90, 110)]
    rand_data_str = str(rand_data)
    rand_data_str = rand_data_str[1:-1]
    file.write(rand_data_str + "\n")
    file.flush()
    os.fsync(file.fileno())
    time.sleep(1)

    print(rand_data_str)
