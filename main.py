import RPi.GPIO as GPIO
from time import sleep
from xbox360controller import Xbox360Controller
from sound import make_sound

LEFT_SPEED_PIN = 12
RIGHT_SPEED_PIN = 13
LEFT_BRAKE_PIN = 26
RIGHT_BRAKE_PIN = 16
LEFT_DIRECTION_PIN = 20
RIGHT_DIRECTION_PIN = 21

LIGHT_PIN = 2

LEFT_PWM = RIGHT_PWM = None

DEADZONE = 0.1

controller = None

GPIO.setmode(GPIO.BCM)

def setup():
    GPIO.setup(LEFT_SPEED_PIN, GPIO.OUT)
    GPIO.setup(RIGHT_SPEED_PIN, GPIO.OUT)
    GPIO.setup(LEFT_BRAKE_PIN, GPIO.OUT)
    GPIO.setup(RIGHT_BRAKE_PIN, GPIO.OUT)
    GPIO.setup(LEFT_DIRECTION_PIN, GPIO.OUT)
    GPIO.setup(RIGHT_DIRECTION_PIN, GPIO.OUT)

    GPIO.setup(LIGHT_PIN, GPIO.OUT)

    global LEFT_PWM, RIGHT_PWM

    LEFT_PWM = GPIO.PWM(LEFT_SPEED_PIN, 1000)
    RIGHT_PWM = GPIO.PWM(RIGHT_SPEED_PIN, 1000)
    LEFT_PWM.start(0)
    RIGHT_PWM.start(0)

    global controller

    controller = Xbox360Controller(0, axis_threshold=DEADZONE)

def set_light(state):
    GPIO.output(LIGHT_PIN, state)

def set_speed(speed_pwm, dir_pin, power):
    if power < 0:
        GPIO.output(dir_pin, GPIO.LOW)
    else:
        GPIO.output(dir_pin, GPIO.HIGH)

    speed_pwm.ChangeDutyCycle(min(100, abs(power * 100)))

def set_brake(brake_pin, brake):
    if brake:
        GPIO.output(brake_pin, GPIO.HIGH)
    else:
        GPIO.output(brake_pin, GPIO.LOW)

def drive(left, right):
    if left == 0:
        set_brake(LEFT_BRAKE_PIN, True)
    else:
        set_brake(LEFT_BRAKE_PIN, False)

    if right == 0:
        set_brake(RIGHT_BRAKE_PIN, True)
    else:
        set_brake(RIGHT_BRAKE_PIN, False)

    set_speed(LEFT_PWM, LEFT_DIRECTION_PIN, left)
    set_speed(RIGHT_PWM, RIGHT_DIRECTION_PIN, right)

def test_forward_backwards():
    while True:
        for power in range(0, 50):
            drive(power / 100, power / 100)
            sleep(0.03)

        sleep(0.2)
        
        for power in range(50, -50, -1):
            drive(power / 100, power / 100)
            sleep(0.03)

        sleep(0.2)
        
        for power in range(-50, 0):
            drive(power / 100, power / 100)
            sleep(0.03)
        
        drive(0, 0)
        sleep(3)

def tank_drive():
    left = -controller.axis_l.y
    right = -controller.axis_r.y
    if abs(left) < DEADZONE:
        left = 0
    if abs(right) < DEADZONE:
        right = 0
    
    drive(left, right)

def arcade_drive():
    speed = -controller.axis_l.y
    turn = controller.axis_r.x
    if abs(speed) < DEADZONE:
        speed = 0
    if abs(turn) < DEADZONE:
        turn = 0
    
    drive(speed + turn, speed - turn)

if __name__ == "__main__":
    setup()
    make_sound(3)

    while True:
        try:
            arcade_drive()
            # tank_drive()
        except KeyboardInterrupt:
            GPIO.cleanup()
            controller.close()
            break
    