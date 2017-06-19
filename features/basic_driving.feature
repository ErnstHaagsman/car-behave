# Created by Ernst.Haagsman at 6/16/2017
Feature: Simulate a basic car
  To show off how BDD works, let's create a sample project which takes the
  classic OO car example, and supercharges it.
  The car should take into account: engine power, basic aerodynamics, rolling
  resistance, grip, and brake force.
  To keep things somewhat simple, the engine will supply constant power (this is
  not realistic, as it results in infinite Torque at 0 RPM)

  Scenario Outline: The car should accelerate at roughly the right rate
    If we take the car's power, weight, and aerodynamic data, we should be able
    to simulate it's acceleration somewhat accurately (let's say within 0.5 seconds)

    Given the car has <power> kw, weighs <weight> kg, has a drag coefficient of <drag>
    And a frontal area of <area> m^2
    When I accelerate to 100 km/h
    Then the time should be within 0.5s of <time>s

    Examples:
    | power  | weight   | drag     | area      | time  | name
    | 90     | 1251     | 0.38     | 1.77      | 6.1   | old Porsche, book example
    | 310    | 2112     | 0.24     | 0.57      | 3.9   | Tesla Model S P85 (Motor trends time)


  Scenario: The car should be able to brake
    The UK highway code says that worst case
    scenario we need to stop from 60mph (27 m/s) in 73m
    Given that the car is moving at 27 m/s
    When I brake at 100% force
    And 10 seconds pass
    Then I should have traveled less than 73 meters


  Scenario: The car should be able to turn right
    Given that the car's heading is 360 deg
    When I turn right at a yaw rate of 20 deg/sec for 2 seconds
    Then the car's heading should be 40 deg


  Scenario: The car should be able to turn left
    Given that the car's heading is 360 deg
    When I turn left at a yaw rate of 20 deg/sec for 2 seconds
    Then the car's heading should be 320 deg