from behave import *

use_step_matcher('re')

@given("that the car is standing still")
def car_is_standing_still(context):
    context.car.speed = 0


@when("I accelerate for (?P<time>\d+) seconds?")
def step_impl(context, time):
    context.car.set_power(100)
    context.car.simulate(time)


@then("the car should be moving")
def step_impl(context):
    assert context.car.speed > 0


@given("that the car is moving at (?P<speed>\d+) m/s")
def step_impl(context, speed):
    context.car.speed = speed


@when("I brake at (?P<brake_force>\d+)% force")
def step_impl(context, brake_force):
    context.car.set_brake(brake_force)


@step("(?P<seconds>\d+) seconds? pass(?:es)?")
def step_impl(context, seconds):
    context.car.simulate(seconds)


@then("I should have traveled less than (?P<distance>\d+) meters")
def step_impl(context, distance):
    assert context.car.odometer < distance


@given("that the car's heading is (?P<heading>\d+) deg")
def step_impl(context, heading):
    context.car.heading = heading


@when("I turn (?P<direction>left|right) at a yaw rate of (?P<rate>\d+) deg/sec for (?P<duration>\d+) seconds")
def step_impl(context, direction, rate, duration):
    if direction == 'left':
        context.car.turn_left(rate)
    else:
        context.car.turn_right(rate)

    context.car.simulate(duration)


@then("the car's heading should be (?P<heading>\d+) deg")
def step_impl(context, heading):
    assert context.car.heading == heading