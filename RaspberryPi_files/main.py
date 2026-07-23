from alarms.alarm_manager import AlarmManager
from datetime import time as dtime
import time

def main():
    alarm_manager = AlarmManager(default_spotify_device_name="Alfred", default_alarm_sound={"playlist": "Upies"})
    try:
        alarm_manager.setup_ble()

        alarm_manager.create_alarm(name="Alarm 1", waking_time=dtime(hour=20, minute=18))

        while True:
            alarm_manager.check_alarms()
            time.sleep(5)
    except KeyboardInterrupt:
        alarm_manager.ble_manager.disconnect()
        alarm_manager.ble_manager.shutdown()


if __name__ == "__main__":
    main()
