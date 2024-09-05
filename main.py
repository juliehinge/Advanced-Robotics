#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
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
        self.right_sensor = ColorSensor(Port.S1)
        self.left_sensor = ColorSensor(Port.S2)
        self.threshold = 33  # 
        self.current_x = 0
        self.current_y = 0
        self.current_angle = 0  # Starts facing positive Y-axis
        self.speed = -100
        self.robot.settings(straight_speed=self.speed)

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




    def follow_line(self):

        directions = ['left', 'straight', 'left', 'right', 'right','straight', 'right']

        while len(directions) > 0:

            left_value = self.left_sensor.reflection()
            right_value = self.right_sensor.reflection()
            print(right_value, left_value)

   
            if left_value < self.threshold and right_value >= self.threshold:
                # Robot is to the right of the line, turn left
                self.robot.drive(-self.speed/2, 50)
                self.ev3.speaker.beep()


            elif right_value < self.threshold and left_value >= self.threshold:
                # Robot is to the left of the line, turn right
                self.robot.drive(-self.speed/2, -50)
                self.ev3.speaker.beep()


            elif left_value < self.threshold and right_value < self.threshold:
                self.ev3.speaker.beep()
                self.move_forward(-40)

                direction = directions.pop(0)
                self.ev3.screen.print(direction, sep=' ', end='\n')

                if direction == 'left':
                    self.turn_to_angle(-90)
                    self.current_angle = 0

                if direction == 'right':
                    self.turn_to_angle(90)
                    self.current_angle = 0

                if direction == 'straight':
                    self.move_forward(-10)

                
            self.move_forward(-10)
           # wait(10)  # Small delay to make the loop manageable


        self.robot.stop()
        self.ev3.speaker.say("Arrived at destination")



robot_controller = RobotController(wheel_diameter=81, axle_track=160)
robot_controller.ev3.speaker.beep()

# Follow the line indefinitely
robot_controller.follow_line()
