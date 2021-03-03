from time import sleep, time
from picamera import PiCamera


class Camera:
    def __init__(self):
        self.camera = PiCamera()

    def make_photo(self):
        self.camera.start_preview()
        sleep(0.7)
        image_file_name = '/home/pi/Desktop/image_%f.jpg' % time()
        self.camera.capture(image_file_name)
        self.camera.stop_preview()

        return image_file_name
