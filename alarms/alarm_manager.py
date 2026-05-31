from alarms.alarm import Alarm
import datetime as dt

class AlarmManager:

    def __init__(self):
        self.__alarms = []

    def create_alarm(self, waking_time : dt.time, sunrise_duration : int = 0, recurence : set[int] = set(), is_active : bool = True):
        """Creates a new alarm with the specified parameters and adds it to the list of handled alarms.
        Args:
            waking_time (dt.time): The time at which the user wants to wake up.
            sunrise_duration (int, optional): The duration in minutes for the sunrise simulation. Defaults to 0.
            recurence (set[int], optional): A set of integers representing the days of the week on which the alarm should recur (0 for Monday, 6 for Sunday). Defaults to an empty set.
            is_active (bool, optional): Whether the alarm is active or not. Defaults to True.
        """
        self.__alarms.append(Alarm(waking_time, sunrise_duration, recurence, is_active))

    def remove_alarm(self, alarm:Alarm):
        self.__alarms.remove(alarm)

    def get_alarms(self):
        return self.__alarms
    
    def set_active(self, alarm:Alarm, is_active: bool = True):
        """Sets the active status of the specified alarm.
        Args:
            alarm (Alarm): The alarm for which to set the active status.
            is_active (bool, optional): The active status to set for the alarm. Defaults to True.
        """
        alarm.is_active = is_active
        if is_active:
            alarm.compute_next_trigger_dt()

    def check_alarms(self, current_time: dt.datetime | None = None):
        """
        Verifies if any alarms are due to trigger based on the current time. If an alarm's next trigger datetime is less than or equal to the current time, it triggers the alarm and recomputes its next trigger datetime.
        Args:
            current_time (dt.datetime | None, optional): The time to check against the alarms. Defaults to the current datetime.
        """
        if current_time is None:
            current_time = dt.datetime.now()

        for alarm in self.__alarms:
            if alarm.next_trigger_dt <= current_time:
                if alarm.is_active:
                    alarm.trigger()
                else:
                    alarm.compute_next_trigger_dt()

