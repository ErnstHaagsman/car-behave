from behave import *
from hamcrest import assert_that, close_to, greater_than, less_than, equal_to

use_step_matcher('re')


@given("that the car is standing still")
def car_is_standing_still(context):
    context.car.speed = 0


@when("I accelerate for (?P<time>\d+) seconds?")
def step_impl(context, time):
    context.car.set_power(100)
    context.car.simulate(time)


@given("the car has (?P<engine_power>\d+) kw, weighs (?P<weight>\d+) kg, has a drag coefficient of (?P<drag>[\.\d]+)")
def step_impl(context, engine_power, weight, drag):
    context.car.engine_power = float(engine_power)
    context.car.weight = float(weight)
    context.car.drag = float(drag)


@given("a frontal area of (?P<area>.+) m\^2")
def step_impl(context, area):
    context.car.frontal_area = float(area)


@when("I accelerate to (?P<speed>\d+) km/h")
def step_impl(context, speed):
    speed_in_ms = float(speed) / 3.6
    context.car.set_power(100)
    while context.car.speed < speed_in_ms:
        context.car.simulate(0.1)


@then("the time should be within (?P<precision>[\d\.]+)s of (?P<time>[\d\.]+)s")
def step_impl(context, precision, time):
    assert_that(context.car.time, close_to(float(time), float(precision)))


@then("the car should be moving")
def step_impl(context):
    assert_that(context.car.speed, greater_than(0))


@given("that the car is moving at (?P<speed>\d+) m/s")
def step_impl(context, speed):
    context.car.speed = float(speed)


@when("I brake at (?P<brake_force>\d+)% force")
def step_impl(context, brake_force):
    context.car.set_brake(brake_force)


@step("(?P<seconds>\d+) seconds? pass(?:es)?")
def step_impl(context, seconds):
    context.car.simulate(seconds)


@then("I should have traveled less than (?P<distance>\d+) meters")
def step_impl(context, distance):
    assert_that(context.car.odometer, less_than(float(distance)))


@given("that the car's heading is (?P<heading>\d+) deg")
def step_impl(context, heading):
    context.car.heading = float(heading)


@when("I turn (?P<direction>left|right) at a yaw rate of (?P<rate>\d+) deg/sec for (?P<duration>\d+) seconds")
def step_impl(context, direction, rate, duration):
    if direction == 'left':
        context.car.turn_left(rate)
    else:
        context.car.turn_right(rate)

    context.car.simulate(duration)


@then("the car's heading should be (?P<heading>\d+) deg")
def step_impl(context, heading):
    assert_that(context.car.heading, equal_to(float(heading)))
