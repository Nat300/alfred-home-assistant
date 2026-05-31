from alarm import Alarm
import datetime as dt

class AlarmManager:

    def __init__(self):
        self.__alarms = []

    def add_alarm(self, alarm:Alarm):
        self.__alarms.append(alarm)

    def remove_alarm(self, alarm:Alarm):
        self.__alarms.remove(alarm)

    def get_alarms(self):
        return self.__alarms
    
    def check_alarms(self, current_time: dt.datetime = dt.datetime.now()):
        """
        Verifies if any alarms are due to trigger based on the current time. If an alarm's next trigger datetime is less than or equal to the current time, it triggers the alarm and recomputes its next trigger datetime.
        Args:
            current_time (dt.datetime, optional): The time to check against the alarms. Defaults to dt.datetime.now().
        """
        for alarm in self.__alarms:
            if alarm.next_trigger_dt <= dt.datetime.fromtimestamp(current_time):
                print(f"Alarm triggered: {alarm}")
                self.trigger_alarm(alarm)

    def trigger_alarm(self, alarm):
        # Placeholder for actual alarm triggering logic (e.g., sound, notification)
        print(f"Alarm triggered: {alarm}")
        alarm.compute_next_trigger_dt()  # Recompute the next trigger time for the alarm
