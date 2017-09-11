import arcade

from bmw540i import BMW_540i

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class CarSim(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title="Car simulator")
        arcade.set_background_color(arcade.color.WHITE)

        self.car = BMW_540i()

        self.rev_counter = arcade.create_text("0 RPM", arcade.color.BLACK, 32)
        self.speedometer = arcade.create_text("0 KM/H", arcade.color.BLACK, 32)
        self.gear_label = arcade.create_text("1", arcade.color.BLACK, 32)

    def update_rpm(self, rpm):
        rpm_text = '{:d}\nRPM'.format(int(rpm))
        if self.rev_counter.text != rpm_text:
            self.rev_counter = arcade.create_text(rpm_text,
                                                  arcade.color.BLACK,
                                                  32,
                                                  align='center',
                                                  anchor_x='center',
                                                  anchor_y='center')

    def update_speed(self, speed):
        speed_text = '{:d}\nKM/H'.format(int(speed))
        if self.speedometer.text != speed_text:
            self.speedometer = arcade.create_text(speed_text,
                                                  arcade.color.BLACK,
                                                  32,
                                                  align='center',
                                                  anchor_x='center',
                                                  anchor_y='center')

    def update_gear(self, gear):
        gear_text = '{:d}'.format(gear)
        if self.gear_label.text != gear_text:
            self.gear_label = arcade.create_text(gear_text,
                                                  arcade.color.BLACK,
                                                  48,
                                                  align='center',
                                                  anchor_x='center',
                                                  anchor_y='center')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.car.set_power(100)
        elif symbol == arcade.key.S:
            self.car.set_brake(100)
        elif symbol == arcade.key.P:
            self.car.gear_up()
        elif symbol == arcade.key.L:
            self.car.gear_down()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.car.set_power(0)
        elif symbol == arcade.key.S:
            self.car.set_brake(0)

    def update(self, dt):
        self.car.simulate(dt)

    def on_draw(self):
        arcade.start_render()

        # Draw RPM
        self.update_rpm(self.car.rpm)
        arcade.render_text(self.rev_counter, 400, 300)

        # Draw speed
        self.update_speed(self.car.speed)
        arcade.render_text(self.speedometer, 600, 300)

        # Draw gear
        self.update_gear(self.car.gear)
        arcade.render_text(self.gear_label, 100, 100)


window = CarSim()
arcade.run()