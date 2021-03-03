from grovepi import pinMode, digitalWrite

def switch_on():
    led = 8
    pinMode(led, "OUTPUT")
    digitalWrite(led, 1)


def switch_off():
    led = 8
    pinMode(led, "OUTPUT")
    digitalWrite(led, 0)
