from time import time, sleep
import grovepi
from camera import Camera
from email_notifier import Emailer
from queue import Queue
from threading import Thread


class USSensor(Thread):
    def __init__(self, camera: Camera, emailer: Emailer, inbox: Queue, outbox: Queue):
        super().__init__()
        self.camera = camera
        self.emailer = emailer
        self.inbox = inbox
        self.outbox = outbox

    def run(self):
        while True:
            if (self.inbox.qsize() != 0):
                self.inbox.get()
                self.read_sensor_for_time_and_make_photo()

    def is_time_window_open(self, start_time):
        return (time() - start_time) < 15


    def read_sensor_for_time_and_make_photo(self):
        distance_treshold_cm = 21
        number_of_pictures = 0
        is_in_range = False
        current_time = time()
        image_file_names = []
        while self.is_time_window_open(current_time) and number_of_pictures < 3:
            current_distance = grovepi.ultrasonicRead(4)
            if not is_in_range and (current_distance < distance_treshold_cm):
                print("Object is in range, making photo...")
                image_file_name = self.camera.make_photo()
                image_file_names.append(image_file_name)
                number_of_pictures += 1
                is_in_range = True
            if is_in_range and (current_distance > distance_treshold_cm):
                print("Object is out of range")
                is_in_range = False
            sleep(0.33)

        self.emailer.send_email_with_images(image_file_names)
