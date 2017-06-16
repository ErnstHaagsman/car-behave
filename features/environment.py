from car import Car


def before_scenario(context, scenario):
    context.car = Car()