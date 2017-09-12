from car import Car, Transmission

GEARS = {
    1: 5.00,
    2: 3.20,
    3: 2.14,
    4: 1.72,
    5: 1.31,
    6: 1.00,
    7: 0.82,
    8: 0.64
}

class BMW_540i(Car):

    def __init__(self):
        super().__init__(weight=1740,  # curb weight, full tank, 90kg driver
                         drag_coefficient=0.26,
                         frontal_area=2.35,
                         brake_force=15000,
                         tire_size='225/55R17',
                         transmission=Transmission(GEARS,
                                                   final_drive=2.93,
                                                   drivetrain_losses=0.15,
                                                   shift_time=0.4))

    TORQUE_CURVE = {
        1000: 318.5,
        1100: 361.9,
        1200: 398.1,
        1300: 428.7,
        1400: 450,
        1500: 450,
        1600: 450,
        1700: 450,
        1800: 450,
        1900: 450,
        2000: 450,
        2100: 450,
        2200: 450,
        2300: 450,
        2400: 450,
        2500: 450,
        2600: 450,
        2700: 450,
        2800: 450,
        2900: 450,
        3000: 450,
        3100: 450,
        3200: 450,
        3300: 450,
        3400: 450,
        3500: 450,
        3600: 450,
        3700: 450,
        3800: 450,
        3900: 450,
        4000: 450,
        4100: 450,
        4200: 450,
        4300: 450,
        4400: 450,
        4500: 450,
        4600: 450,
        4700: 450,
        4800: 450,
        4900: 450,
        5000: 450,
        5100: 449.4,
        5200: 440.7,
        5300: 432.4,
        5400: 424.4,
        5500: 416.7,
        5600: 409.2,
        5700: 402.1,
        5800: 395.1,
        5900: 388.4,
        6000: 382,
        6100: 375.7,
        6200: 369.6,
        6300: 363.8,
        6400: 358.1,
        6500: 352.6,
        6600: 345.8,
        6700: 336.6,
        6800: 324.9,
        6900: 310.9,
        7000: 294.7,
    }

    def get_engine_torque(self, rpm):
        min_rpm = min(self.TORQUE_CURVE.keys())
        max_rpm = max(self.TORQUE_CURVE.keys())

        if rpm < min_rpm:
            return self.TORQUE_CURVE[min_rpm]
        elif rpm > max_rpm:
            return self.TORQUE_CURVE[max_rpm]

        # Calculate the nearest 100 rpm to the requested amount
        rpm_hundred = round(rpm / 100)

        return self.TORQUE_CURVE[int(rpm_hundred * 100)]

    def get_engine_idle_rpm(self):
        return 1100
