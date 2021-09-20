from ddcmath.psychrometric import enthalpy, dewpoint, temperature_from_humidity_and_dewpoint, humidity_from_wetbulb_and_drybulb
from ddcmath.tolerance import abs_relative_error

def test_enthalpy():
    pass


def test_dewpoint():
    assert (dewpoint(temp=20, hum=60, SI=True) - 12) < 0.01
    assert (dewpoint(temp=40, hum=65, SI=False) - 29.22) < 0.01

def enthlapy():
    assert abs_relative_error(humidity_from_wetbulb_and_drybulb(Td=20, Tw=20),100) < 0.01
    assert abs_relative_error(humidity_from_wetbulb_and_drybulb(Td=30, Tw=20),38.957) < 0.01
    assert abs_relative_error(humidity_from_wetbulb_and_drybulb(Td=20, Tw=15),58.376) < 0.01