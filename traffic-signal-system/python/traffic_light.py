from threading import Lock
from signal import Signal

class TrafficLight:
    def __init__(self, id, red_duration, yellow_duration, green_duration):
        self.id = id
        self.current_signal = Signal.RED
        self.red_duration = red_duration
        self.yellow_duration = yellow_duration
        self.green_duration = green_duration
        self.lock = Lock()
 
    def get_current_signal(self):
        return self.current_signal
 
    def change_signal(self, new_signal):
        with self.lock:
            self.current_signal = new_signal
            self.notify_observers()
 
    def notify_observers(self):
        # Sent event to all registered observers
        pass
