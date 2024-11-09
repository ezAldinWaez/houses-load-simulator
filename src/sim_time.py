from datetime import datetime, timedelta
import time


class SimulationTime:
    def __init__(self, time_factor: float):
        """
        Parameters
        ----------
        - timeFactor : Time acceleration factor (in sec).
        """
        self.time_factor = time_factor
        self.start_real_time = time.time()
        self.paused_at = None
        self.pause_duration = 0

    def get_elapsed(self) -> float:
        """
        Return the elapsed simulation time (number of seconds).
        """
        if self.paused_at is not None:
            return (self.paused_at - self.start_real_time - self.pause_duration) * self.time_factor
        return (time.time() - self.start_real_time - self.pause_duration) * self.time_factor

    def get_time(self) -> datetime:
        """
        Return the current simulation datetime.
        """
        return datetime.now() + timedelta(seconds=self.get_elapsed())

    def pause(self):
        """
        Pause the simulation time.
        """
        if self.paused_at is None:
            self.paused_at = time.time()

    def resume(self):
        """
        Resume the simulation time.
        """
        if self.paused_at is not None:
            self.pause_duration += time.time() - self.paused_at
            self.paused_at = None
