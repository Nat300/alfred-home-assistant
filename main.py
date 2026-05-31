from alarms.alarm_manager import AlarmManager
from datetime import time,datetime
from time import sleep

alarm_manager = AlarmManager()

alarm_manager.create_alarm(waking_time = time(hour=17,minute=30), sunrise_duration = 30, recurence = {5,6}, is_active = True)

while True:
    alarm_manager.check_alarms()
    sleep(5)
