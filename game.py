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

    def update_rpm(self, rpm):
        rpm_text = '{}\nRPM'.format(rpm)
        if self.rev_counter.text != rpm_text:
            self.rev_counter = arcade.create_text(rpm_text,
                                                  arcade.color.BLACK,
                                                  32,
                                                  align='center',
                                                  anchor_x='center',
                                                  anchor_y='center')

    def update_speed(self, speed):
        speed_text = '{}\nKM/H'.format(speed)
        if self.speedometer.text != speed_text:
            self.speedometer = arcade.create_text(speed_text,
                                                  arcade.color.BLACK,
                                                  32,
                                                  align='center',
                                                  anchor_x='center',
                                                  anchor_y='center')


    def update(self, dt):
        self.car.simulate(dt)

    def on_draw(self):
        arcade.start_render()

        # Draw RPM
        self.update_rpm(self.car.rpm)
        arcade.render_text(self.rev_counter, 400, 600)

        # Draw speed
        self.update_speed(self.car.speed)
        arcade.render_text(self.speedometer, 600, 600)


window = CarSim()
arcade.run()