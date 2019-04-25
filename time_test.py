import time


start_time = time.localtime(time.time())
sec0 = start_time[3] * 3600 + start_time[4] * 60 + start_time[5]
sec_last = 0
while 1:
    current_time = time.localtime(time.time())
    sec = current_time[3] * 3600 + current_time[4] * 60 + current_time[5]
    if sec_last != sec:
        print sec - sec0

    sec_last = sec