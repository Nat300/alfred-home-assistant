from alarms.alarm_manager import AlarmManager
from datetime import time
from time import sleep

alarm_manager = AlarmManager(default_spotify_device_name="Alfred", default_alarm_sound={"playlist": "Upies"})

alarm_manager.create_alarm(name="Alarm 1", waking_time = time(hour=8,minute=10), sound={"track": "american pie", "artist": "don mclean"})

while True:
    alarm_manager.check_alarms()
    sleep(5)
 