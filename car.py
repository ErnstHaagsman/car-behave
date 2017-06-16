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

    def __init__(self, engine_power=270, weight=1251, drag_coefficient=0.38, frontal_area=1.77, brake_force=10_000):
        """
        Create a car to simulate.

        Limitations: The car has perfect traction control and will exert exactly the tire grip limit if too much
        power is applied (longitudinally) and infinite lateral grip. Furthermore, engine power is fully linear (somewhat
        realistic for electric cars)

        :param engine_power:        The engine's power in kW
        :param weight:              The car's curb weight in kg
        :param drag_coefficient:    Cw value (dimensionless)
        :param frontal_area:        Frontal area of the car in m^2
        :param brake_force:         Force the brakes can exert in N
        """
        # Car status
        self.power = 0
        self.braking = 0
        self.speed = 0
        self.odometer = 0
        self.heading = 360
        self.yaw_rate = 0
        self.time = 0.0

        # Car characteristics
        self.engine_power = engine_power
        self.weight = weight
        self.drag_coefficient = drag_coefficient
        self.frontal_area = frontal_area
        self.brake_force = brake_force

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

    def simulate(self, time):
        """
        Simulate the passing of time
        :param time: Time in seconds
        """
        start_time = self.time
        end_time = self.time + float(time)

        while self.time < end_time:
            self._simulate_step(self.STEP_SIZE)

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

        # Engine power, needs to be multiplied by 1k to get watts from kilowatts
        P_engine = (self.power / 100) * self.engine_power * 1_000

        # Power = Force * Velocity, so Force = Power / Velocity.
        # To deal with v = 0, let's just say the forward force at V=0 is equal to braking force * power setting
        if self.speed == 0.0:
            F_engine = self.brake_force * (self.power / 100)
        else:
            F_engine = P_engine / self.speed

        # Brake force
        F_brake = (self.braking / 100) * self.brake_force

        # Resultant force is: + F_engine - F_air - F_roll - F_brake, where positive is forward
        force = F_engine - F_air - F_roll - F_brake

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

        # Deal with turning
        self.heading += self.yaw_rate

        if self.heading > 360:
            self.heading -= 360
        elif self.heading < 0:
            self.heading += 360

        self.time += delta_T
