import RPi.GPIO as GPIO
from time import time, sleep
import grovepi
from threading import Thread
from queue import Queue

feed_cycle_seconds = 30
control_pins = [29, 31, 33, 35]


class Stepmotor(Thread):
    def __init__(self, inbox: Queue, outbox: Queue):
        super().__init__()
        self.inbox = inbox
        self.outbox = outbox
        self.init_pins()
        self.is_food_full = False
        self.last_time_fed = 0

    def init_pins(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def spin_motor(self, quarter_revs_required):
        halfsteps_in_quarter_rev = 128
        halfsteps_required = quarter_revs_required * halfsteps_in_quarter_rev
        halfstep_time_interval = 0.003
        halfstep_seq = [
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 1]
        ]
        halfsteps_done = 0
        while halfsteps_done <= halfsteps_required:
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                sleep(halfstep_time_interval)
            halfsteps_done += 1

    def run(self):
        while True:
            self.check_food_level()
            if self.should_feed():
                self.feed()

    def should_feed(self):
        is_time_to_feed = self.is_time_to_feed()
        if(is_time_to_feed):
            print("is_full = %s" % self.is_food_full)
            return is_time_to_feed and self.is_food_full
        return False

    def check_food_level(self):
        while self.inbox.qsize() > 0:
            last_message = self.inbox.get()
            self.is_food_full = last_message.get("is_full")

    def is_time_to_feed(self):
        if (time() - self.last_time_fed > feed_cycle_seconds):
            print("Its time to feed")
            self.last_time_fed = time()
            return True
        else:
            return False

    def feed(self):
        print("Feeding...")
        self.spin_motor(1)
        self.outbox.put({"message": "feeding completed"})
