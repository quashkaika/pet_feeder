from queue import Queue
from time import sleep
from threading import Thread
from light import switch_on, switch_off
from grovepi import pinMode, digitalRead

level_check_interval_seconds = 3
sensor_port = 3

class IRSensor(Thread):
    def __init__(self, outbox: Queue):
        super().__init__()
        self.outbox = outbox
        pinMode(sensor_port, "INPUT")

    def run(self):
        while True:
            sleep(level_check_interval_seconds)
            sensor_output = digitalRead(sensor_port)
            self.outbox.put({"is_full": not sensor_output})
            if sensor_output:
                switch_on()
            else:
                switch_off()
