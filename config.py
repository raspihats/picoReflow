import logging
import interface

########################################################################
#
#   General options

### Logging
log_level = logging.INFO
log_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'

### Server
listening_ip = "0.0.0.0"
listening_port = 8081

### Cost Estimate
kwh_rate        = 0.26  # Rate in currency_type to calculate cost to run job
currency_type   = "EUR"   # Currency Symbol to show when calculating cost to run job

########################################################################
#
#   GPIO Setup (BCM SoC Numbering Schema)
#
#   Check the RasPi docs to see where these GPIOs are
#   connected on the P1 header for your board type/rev.
#   These were tested on a Pi B Rev2 but of course you
#   can use whichever GPIO you prefer/have available.

### Digital Outputs
# gpio_heat = 11  # Switches zero-cross solid-state-relay
# heating_element = interface.RpiDigitalOutput(11)
heating_element = interface.AI3tcDQ4rlyDigitalOutput(0x70, [0, 1])

# gpio_cool = 10  # Regulates PWM for 12V DC Blower
gpio_cool = interface.AI3tcDQ4rlyDigitalOutput(0x70, 2)
# gpio_air  = 9   # Switches 0-phase det. solid-state-relay
gpio_air = interface.AI3tcDQ4rlyDigitalOutput(0x70, 3)

heater_invert = 0 # switches the polarity of the heater control

### Inputs
gpio_door = 18

### Thermocouple Adapter selection:
#### Thermocouple Connection (using bitbang interfaces)
#thermocouple = interface.MAX6675(cs=27, clock=22, data=17, scale='c')
#thermocouple = interface.MAX31855(cs=27, clock=22, data=17, scale='c')

#### Thermocouple SPI Connection (using adafrut drivers + kernel SPI interface)
# thermocouple = interface.MAX31855Ada(chip_id)

#### Thermocouple using AI3tcDQ4rly I2C-HAT from raspihats.com
thermocouple = interface.AI3tcDQ4rlyThermocoupleInput(0x70, 0)

### amount of time, in seconds, to wait between reads of the thermocouple
sensor_time_wait = .5


########################################################################
#
#   PID parameters

pid_kp = 0.1  # Proportional
pid_ki = 0.1  # Integration
pid_kd = 0.4  # Derivative

########################################################################
#
#   Simulation parameters

sim_t_env      = 25.0   # deg C
sim_c_heat     = 100.0  # J/K  heat capacity of heat element
sim_c_oven     = 2000.0 # J/K  heat capacity of oven
sim_p_heat     = 3500.0 # W    heating power of oven
sim_R_o_nocool = 1.0    # K/W  thermal resistance oven -> environment
sim_R_o_cool   = 0.05   # K/W  " with cooling
sim_R_ho_noair = 0.1    # K/W  thermal resistance heat element -> oven
sim_R_ho_air   = 0.05   # K/W  " with internal air circulation


########################################################################
#
#   Time and Temperature parameters

temp_scale          = "c" # c = Celsius | f = Fahrenheit - Unit to display
time_scale_slope    = "s" # s = Seconds | m = Minutes | h = Hours - Slope displayed in temp_scale per time_scale_slope
time_scale_profile  = "s" # s = Seconds | m = Minutes | h = Hours - Enter and view target time in time_scale_profile
