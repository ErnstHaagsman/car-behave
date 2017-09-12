# Millimeters per inch
import re

import math

MM_PER_INCH = 25.4

# Millimeters per meter
MM_PER_M = 1000

class Car:
    STEP_SIZE = 0.1


    # Coefficient of friction for rolling resistance
    C_RR = 0.015

    # Coefficient of friction for tire grip
    MU = 0.9

    # Air density in kg/m^3
    RHO = 1.2

    # Gravity on earth
    G = 9.81

    def __init__(self,
                 weight=1251,
                 drag_coefficient=0.38,
                 frontal_area=1.77,
                 brake_force=10000,
                 tire_size='225/55R17',
                 transmission=None):
        """
        Create a car to simulate.

        Limitations: The car has perfect traction control and will exert exactly the tire grip limit if too much
        power is applied (longitudinally) and infinite lateral grip. Furthermore, engine power is fully linear (somewhat
        realistic for electric cars)

        :param weight:              The car's curb weight in kg
        :param drag_coefficient:    Cd value (dimensionless)
        :param frontal_area:        Frontal area of the car in m^2
        :param brake_force:         Force the brakes can exert in N
        :param tire_size:           The tire size, as written on the sidewall
        """
        # Car status
        self.gear = 1
        self.power = 0  # % throttle applied
        self.braking = 0  # % brakes applied
        self.speed = 0  # in m/s
        self.odometer = 0  # in m
        self.heading = 360
        self.yaw_rate = 0  # in deg/sec
        self.time = 0.0  # in seconds
        self.rpm = self.get_engine_idle_rpm()

        # Car characteristics
        self.weight = weight
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.brake_force = brake_force
        self.transmission = transmission

        # Decode the tire
        pattern = """(\d{3})/(\d{2})R(\d{2})"""
        match = re.match(pattern, tire_size)
        if match:
            self.tire_width = int(match.group(1))
            self.tire_aspect = int(match.group(2))
            self.rim_size = int(match.group(3))
        else:
            raise ValueError("Please specify a valid tire size (e.g. 255/45R18)")

    def get_engine_torque(self, rpm):
        """
        Calculate the engine torque generated at a specified engine speed

        :param rpm: {int} Input engine speed
        :return: {float} The torque delivered from the engine in newton meters at the specified engine speed
        """
        return 0.0

    def get_engine_idle_rpm(self):
        return 0

    def get_engine_redline_rpm(self):
        return 7000

    def get_tire_force(self, width, aspect, diameter, torque):
        """
        Returns the force applied by the tire, as a result of a torque
        :param int width: The width of the tire, in millimeters
        :param int aspect: The aspect ratio of the tire, number 0-100
        :param int diameter: The diameter of the rim, in inches
        :param float torque: The torque applied to the wheel
        :return: Force in newtons
        :rtype: float
        """
        tirewall_height = float(width) * (float(aspect) / 100)
        wheel_diameter = diameter * MM_PER_INCH + tirewall_height

        radius = wheel_diameter / 2

        # The force at the bottom of the tire is the torque (N*m) / radius (m)
        return torque / (radius / MM_PER_M)

    def get_tire_rpm(self, width, aspect, diameter, speed):
        """
        Returns the tire rotational speed, for a given forward speed
        :param width: Tire width, in millimeters
        :param aspect: The aspect ratio of the tire, number 0-100
        :param diameter: The diameter of the rim, in inches
        :param speed: Speed of the car in m/s
        :return: Rotational speed of the wheel, in rpm
        """

        tirewall_height = float(width) * (float(aspect) / 100)
        wheel_diameter = diameter * MM_PER_INCH + tirewall_height  # in mm

        wheel_diameter_meters = wheel_diameter / 1000  # in m
        wheel_circumference = math.pi * wheel_diameter_meters  # in m

        meters_per_minute = speed * 60  # m/s to m/min

        # Return the amount of wheel circumferences (rotations) we're driving every minute
        return meters_per_minute / wheel_circumference

    def set_power(self, amount):
        """
        Sets the power level as a percentage, think of it as how deeply you've pressed the gas pedal
        :param amount: Required amount of power between 0 and 100 (percent)
        """
        self.power = float(amount)

    def set_brake(self, amount):
        """
        Sets the desired amount of braking. Percentage of full braking force.
        :param amount: Required amount of brakes between 0 and 100 (percent)
        """
        self.braking = float(amount)

    def turn_left(self, rate):
        """
        Start turning left at the specified rate
        :param rate: Yaw rate in degrees / second
        """
        self.yaw_rate = - float(rate)

    def turn_right(self, rate):
        """
        Start turning right at the specified rate
        :param rate: Yaw rate in degrees / second
        """
        self.yaw_rate = float(rate)

    def gear_up(self):
        self.transmission.gear_up()

    def gear_down(self):
        self.transmission.gear_down()

    def simulate(self, time):
        """
        Simulate the passing of time
        :param time: Time in seconds
        """

        if time > self.STEP_SIZE:
            start_time = self.time
            end_time = self.time + float(time)

            while self.time < end_time:
                self._simulate_step(self.STEP_SIZE)
        else:
            self._simulate_step(time)

    def _simulate_step(self, delta_T):
        # Update the state

        # We covered some distance
        self.odometer += self.speed * delta_T

        # To calculate acceleration, we need the weight in newtons, assuming we're on earth:
        weight_N = self.weight * self.G

        # Calculate longitudinal forces
        # Roll resistance
        F_roll = self.C_RR * weight_N

        # Air resistance
        F_air = 0.5 * self.drag_coefficient * self.frontal_area * self.RHO * pow(self.speed, 2)

        # Calculate engine speed
        wheel_rpm = self.get_tire_rpm(self.tire_width, self.tire_aspect, self.rim_size, self.speed)
        self.transmission.set_driveshaft_speed(wheel_rpm)
        engine_speed = self.transmission.engine_shaft_speed

        if engine_speed < self.get_engine_idle_rpm():
            engine_speed = self.get_engine_idle_rpm()

        # Find torque at engine
        T_engine = self.get_engine_torque(engine_speed) * (self.power / 100)

        # Rev limiter
        if engine_speed >= self.get_engine_redline_rpm():
            self.gear_up()
            T_engine = 0

        self.rpm = engine_speed

        # Subtract drivetrain losses, and multiply by transmission ratio to get wheel torque
        self.transmission.set_engine_torque(T_engine)
        T_wheel = self.transmission.driveshaft_torque

        # Find force at the contact patch
        F_wheel = self.get_tire_force(self.tire_width, self.tire_aspect, self.rim_size, T_wheel)

        # Brake force
        F_brake = (self.braking / 100) * self.brake_force

        # Resultant force is: + F_engine - F_air - F_brake, where positive is forward
        force = F_wheel - F_air - F_brake - F_roll

        # Our tires have a grip limit, determined by friction and (aerodynamic) weight
        F_max = self.MU * weight_N

        if force > F_max:
            force = F_max
        elif force < -F_max:
            force = -F_max

        # Force = mass * acceleration, so acceleration (m/s^2) = force (N) / mass (kg)
        acceleration = force / self.weight

        # The cars new speed:
        self.speed += acceleration * delta_T

        # No reverse gear, no negative speed
        if self.speed < 0:
            self.speed = 0

        # Deal with turning
        self.heading += self.yaw_rate

        if self.heading > 360:
            self.heading -= 360
        elif self.heading < 0:
            self.heading += 360

        self.time += delta_T


class Transmission:
    def __init__(self, gear_ratios, final_drive, shift_speed, drivetrain_losses):
        self.ratios = gear_ratios
        self.final_drive = final_drive
        self.shift_speed = shift_speed
        self.drivetrain_losses = drivetrain_losses

        self.gear_count = len(self.ratios)

        # state
        self.engine_shaft_speed = 0
        self.driveshaft_speed = 0
        self.engine_torque = 0
        self.driveshaft_torque = 0
        self.gear = 1

    def _total_ratio(self):
        return self.ratios[self.gear] * self.final_drive

    def set_driveshaft_speed(self, speed):
        """
        :param speed: Speed in rpm
        :return:
        """
        self.engine_shaft_speed = speed * self._total_ratio()

    def set_engine_torque(self, torque):
        """
        Correctly sets the torque at the driveshaft, taking into account the gear and losses
        :param torque: Input torque in Nm
        :return:
        """
        self.driveshaft_torque = torque * self._total_ratio() * (1 - self.drivetrain_losses)

    def gear_up(self):
        if self.gear + 1 < self.gear_count:
            self.gear += 1

    def gear_down(self):
        if self.gear > 1:
            self.gear -= 1