#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import math

class RobotController:
    def __init__(self, wheel_diameter, axle_track):
        self.ev3 = EV3Brick()
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.D)
        self.robot = DriveBase(self.left_motor, self.right_motor, wheel_diameter, axle_track)
        self.current_x = 0
        self.current_y = 0
        self.current_angle = 0  # Starts facing positive Y-axis

    def move_forward(self, distance_cm):
        self.robot.straight(distance_cm)
        self.current_x += distance_cm * math.cos(math.radians(self.current_angle))
        self.current_y += distance_cm * math.sin(math.radians(self.current_angle))

    def turn_to_angle(self, target_angle):
        turn_angle = target_angle - self.current_angle
        self.robot.turn(-turn_angle)
        self.current_angle = target_angle



    def turn_relative_to_start(self, relative_angle):
        target_angle = self.current_angle + relative_angle
        self.turn_to_angle(target_angle)



    def move_to_coordinate(self, target_x, target_y):
        delta_x = target_x - self.current_x
        delta_y = target_y - self.current_y

        # Calculate the angle from the current position to the target
        target_angle = math.degrees(math.atan2(delta_y, delta_x))
        distance = math.sqrt(delta_x**2 + delta_y**2)

        # Turn to the target angle
        self.turn_to_angle(target_angle)
        
        # Move forward to the target coordinate
        self.move_forward(distance)

# Example usage
robot_controller = RobotController(wheel_diameter=81, axle_track=160)
robot_controller.ev3.speaker.beep()

# Move to coordinate (200, -220)
robot_controller.move_to_coordinate(-1250, 0)

robot_controller.turn_relative_to_start(30)