from alarms.alarm_manager import AlarmManager
from datetime import time
from time import sleep

alarm_manager = AlarmManager()

alarm_manager.create_alarm(waking_time = time(hour=9,minute=46))

while True:
    alarm_manager.check_alarms()
    sleep(5)
