from unittest import TestCase
from bmw540i import BMW_540i

class BMW_test(TestCase):
    def test_acceleration_100(self):
        car = BMW_540i()
        car.set_power(100)
        car.simulate(5)
        speed_kmh = car.speed * 3.6
        print(speed_kmh)
        assert speed_kmh > 95 and speed_kmh < 105

    def test_acceleration_80(self):
        car = BMW_540i()
        car.set_power(100)
        car.simulate(3.5)
        speed_kmh = car.speed * 3.6
        print(speed_kmh)
        assert speed_kmh > 75 and speed_kmh < 85

    def test_acceleration_160(self):
        car = BMW_540i()
        car.set_power(100)
        car.simulate(11.4)
        speed_kmh = car.speed * 3.6
        print(speed_kmh)
        assert speed_kmh > 155 and speed_kmh < 165

    def test_acceleration_200(self):
        car = BMW_540i()
        car.set_power(100)
        car.simulate(19)
        speed_kmh = car.speed * 3.6
        print(speed_kmh)
        assert speed_kmh > 195 and speed_kmh < 205