#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

class RobotController:
    def __init__(self, wheel_diameter, axle_track):
        robot_controller.ev3.speaker.beep()
        self.ev3 = EV3Brick()
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.D)
        self.robot = DriveBase(self.left_motor, self.right_motor, wheel_diameter, axle_track)
        self.line_sensor = LightSensor(Port.S3)
        self.speed = -100
        self.robot.settings(straight_speed=self.speed)


    def follow_line(self):
        target = 4
        error = 0
        integral = 0
        kp = 1
        ki = 0
        kd = 0

        while True:
            value = self.line_sensor.reflection()
            self.ev3.screen.print(value, sep=' ', end='\n')

            error_old = error
            error = target - value
            integral = integral + error
            derivative = error - error_old

            steering = kp*error + ki*integral + kd*derivative

            self.robot.drive(self.speed, steering)


robot_controller = RobotController(wheel_diameter=81, axle_track=160)

# Follow the line indefinitely
robot_controller.follow_line()
