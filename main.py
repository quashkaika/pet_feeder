from multiprocessing import Queue
from ir_sensor import IRSensor
from us_sensor import USSensor
from stepmotor import Stepmotor
from camera import Camera
from email_notifier import Emailer

def main():
    us_sensor_inbox = Queue()
    motor_inbox = Queue()
    emailer_inbox = Queue()
    camera = Camera()

    ir_sensor = IRSensor(motor_inbox)
    stepmotor = Stepmotor(motor_inbox, us_sensor_inbox)
    emailer = Emailer()
    us_sensor = USSensor(camera, emailer, us_sensor_inbox, emailer_inbox)

    us_sensor.start()
    ir_sensor.start()
    stepmotor.start()

main()
