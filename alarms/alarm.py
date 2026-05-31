import datetime as dt
from enum import Enum
from typing import Literal

class Alarm:

    def __init__(self, waking_time : dt.time, sunrise_duration : int = 0, recurence : set[int] = set(), is_active : bool = True):
        """
        Initializes an Alarm object with the specified waking time and optional sunrise duration, recurrence pattern, and active status.
        Args:
            waking_time (dt.time): The time at which the user wants to wake up.
            sunrise_duration (int, optional): The duration in minutes for the sunrise simulation. Defaults to 0.
            recurence (set[int], optional): A set of integers representing the days of the week on which the alarm should recur (0 for Monday, 6 for Sunday). Defaults to an empty set.
            is_active (bool, optional): Whether the alarm is active or not. Defaults to True.
        """
        self.waking_time = waking_time
        self.sunrise_duration = dt.timedelta(minutes=sunrise_duration)
        self.recurence = recurence
        self.is_active = is_active
        self.compute_next_trigger_dt()

    def __str__(self):
        return f"Alarm set for {self.waking_time} with sunrise duration of {self.sunrise_duration} minutes and recurence pattern of {self.recurence}"

    def compute_next_trigger_dt(self):
        """
        Calculates the next trigger datetime for the alarm based on the current time, waking time, sunrise duration, and recurrence pattern.
        """
        now = dt.datetime.now()
        trigger_time = (dt.datetime.combine(dt.date.today(), self.waking_time) - self.sunrise_duration).time() #converts the waking time into a datetime object, subtracts the sunrise duration, and converts it back to a time object to get the actual trigger time for the alarm

        candidate_trigger = dt.datetime.combine(now.date(), trigger_time)

        if self.recurence == set():
            if candidate_trigger < now:
                self.next_trigger_dt = candidate_trigger + dt.timedelta(days=1)
            else:
                self.next_trigger_dt = candidate_trigger
        else:
            current_weekday = now.weekday() # .weekday() returns the day of the week as an integer, where Monday is 0 and Sunday is 6, matching the format of the recurence set
            candidate_weekday = candidate_trigger.weekday()

            if current_weekday not in self.recurence or candidate_trigger < now:
                days_until_next_recurence = min((day - current_weekday) % 7 for day in self.recurence) 
                self.next_trigger_dt =  candidate_trigger + dt.timedelta(days=days_until_next_recurence)
            elif candidate_trigger > now and candidate_weekday in self.recurence:
                self.next_trigger_dt = candidate_trigger
            
    