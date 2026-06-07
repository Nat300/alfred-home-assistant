from alarms.alarm import Alarm
from alarms.spotify_controler import SpotifyController
import datetime as dt

class AlarmManager:

    def __init__(self,default_spotify_device_name: str, default_alarm_sound: dict[str, str]):
        """
        Initializes an AlarmManager object with a default alarm sound.
        Args:
            default_spotify_device_name (str): The name of the Spotify device to play alarms on.
            default_alarm_sound (dict[str, str]): A dictionary containing the default sound settings for alarms. The dictionary should have the same format as the "sound" parameter in the Alarm class, with keys such as "track", "artist" or "playlist" and corresponding values for the default sound to play when an alarm is triggered without a specific sound setting.
        """
        self.__alarms = []
        self.default_alarm_sound = default_alarm_sound
        self.spotify_controller = SpotifyController(default_device_name=default_spotify_device_name)

    def create_alarm(self, waking_time : dt.time, name:str = "Unnamed Alarm", sunrise_duration : int = 0, recurence : set[int] = None, is_active : bool = True, sound: dict[str, str] | None = None):
        """Creates a new alarm with the specified parameters and adds it to the list of handled alarms.
        Args:
            waking_time (dt.time): The time at which the user wants to wake up.
            name (str): The name of the alarm.
            sunrise_duration (int, optional): The duration in minutes for the sunrise simulation. Defaults to 0.
            recurence (set[int], optional): A set of integers representing the days of the week on which the alarm should recur (0 for Monday, 6 for Sunday). Defaults to an empty set.
            is_active (bool, optional): Whether the alarm is active or not. Defaults to True.
            sound (dict[str, str] | None, optional): A dictionary containing the sound settings for the alarm. If not provided, the default alarm sound will be used. Defaults to None.
        """
        self.__alarms.append(Alarm(waking_time, name, sunrise_duration, recurence, is_active, sound))

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
            print(f"Alarm activated: {alarm}")
            alarm.compute_next_trigger_dt()
        else:
            print(f"Alarm deactivated: {alarm}")

    def check_alarms(self, current_time: dt.datetime | None = None):
        """
        Verifies if any alarms are due to trigger based on the current time. If an alarm's next trigger datetime is less than or equal to the current time, it triggers the alarm and recomputes its next trigger datetime.
        Args:
            current_time (dt.datetime | None, optional): The time to check against the alarms. Defaults to the current datetime.
        """

        if current_time is None:
            current_time = dt.datetime.now()

        for alarm in self.__alarms:
            if alarm.is_active and alarm.next_trigger_dt <= current_time:
                self.trigger_alarm(alarm)

    def trigger_alarm(self, alarm:Alarm):
        self.spotify_controller.play(**(alarm.sound if alarm.sound else self.default_alarm_sound)) # first chooses the dictionary to be used, the unpacks it into keyword arguments for the play function
        if alarm.recurence is None:
            alarm.is_active = False
            print(f"Alarm deactivated: {alarm}")
        else:
            alarm.compute_next_trigger_dt()  
        

