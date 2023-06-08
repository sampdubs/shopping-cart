import RPi.GPIO as GPIO
from time import sleep, time

SPEAKER_PIN = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

def make_sound(duration, frequency=440):
    start = time()
    state = True
    while (time() - start) < duration:
        GPIO.output(SPEAKER_PIN, state)
        state = not state
        sleep(1 / frequency)

if __name__ == "__main__":
    make_sound(5)
    GPIO.cleanup()