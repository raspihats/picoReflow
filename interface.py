import abc
# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

class DigitalOutput(object):

    @abc.abstractmethod
    def set_state(self, state):
        pass

    @abc.abstractmethod
    def get_state(self):
        pass


class RpiDigitalOutput(DigitalOutput):
    def __init__(self, gpio):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(gpio, GPIO.OUT)
        self.gpio = gpio

    def set_state(self, state):
        import RPi.GPIO as GPIO
        if state:
            GPIO.output(self.gpio, GPIO.HIGH)
        else:
            GPIO.output(self.gpio, GPIO.LOw)

    def get_state(self):
        pass


class AI3tcDQ4rlyDigitalOutput(DigitalOutput):
    def __init__(self, address, ch):
        from raspihats.i2c_hats import AI3tcDQ4rly
        self.board = AI3tcDQ4rly(address)
        self.ch = ch

    def set_state(self, state):
        if isinstance(self.ch, list):
            for channel in self.ch:
                self.board.dq[channel].state = state
        else:
            self.board.dq[self.ch].state = state

    def get_state(self):
        pass


class ThermocoupleInput(object):

    @abc.abstractmethod
    def get_temperature(self):
        pass


class MAX6675(ThermocoupleInput):
    def __init__(self, cs, clock, data, scale):
        import max6675
        self.max = max6675.MAX6675(cs, clock, data, scale)

    def get_temperature(self):
        return self.max.get()


class MAX31855(ThermocoupleInput):
    def __init__(self, cs, clock, data, scale):
        import max31855
        self.max = max31855.MAX31855(cs, clock, data, scale)

    def get_temperature(self):
        return self.max.get()


class MAX31855Ada(ThermocoupleInput):
    def __init__(self, chip_id):
        import max31855spi
        self.max = max31855spi.MAX31855SPI(spi_dev=SPI.SpiDev(port=0, device=chip_id))

    def get_temperature(self):
        return self.max.get()


class AI3tcDQ4rlyThermocoupleInput(ThermocoupleInput):
    def __init__(self, address, channel):
        from raspihats.i2c_hats import AI3tcDQ4rly
        self.board = AI3tcDQ4rly(address)
        self.channel = channel

    def get_temperature(self):
        return self.board.ai.channels[self.channel]


    # if config.AI3tcDQ4rly:
    #     class ThermocoupleAdaptor(object):
    #         def __init__(self, address, channel):
    #             self.board = AI3tcDQ4rly(address)
    #             self.channel = channel
    #
    #         def get(self):
    #             return self.board.ai.channels[self.channel]
    #
    #     self.thermocouple = ThermocoupleAdaptor(0x70, 0)
