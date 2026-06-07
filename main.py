from alarms.alarm_manager import AlarmManager
from datetime import time
from time import sleep

alarm_manager = AlarmManager(default_spotify_device_name="Alfred", default_alarm_sound={"playlist": "Upies"})

alarm_manager.create_alarm(name="Alarm 1", waking_time = time(hour=22,minute=46), sound={"track": "I wanna be yours"})

while True:
    alarm_manager.check_alarms()
    sleep(5)
