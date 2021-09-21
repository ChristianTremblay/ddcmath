from ddcmath.psychrometric import (
    enthalpy,
    dewpoint_from_temperature_and_humidity,
    temperature_from_humidity_and_dewpoint,
    humidity_from_wetbulb_and_drybulb,
)
from ddcmath.tolerance import abs_relative_error


def test_enthalpy():
    pass


def test_dewpoint():
    assert (
        dewpoint_from_temperature_and_humidity(
            temperature=20, humidity=60, SI=True
        ).magnitude
        - 12
    ) < 0.01
    assert (
        dewpoint_from_temperature_and_humidity(
            temperature=40, humidity=65, SI=False
        ).magnitude
        - 29.22
    ) < 0.01


def test_humidity():
    assert (
        abs_relative_error(
            humidity_from_wetbulb_and_drybulb(temperature=20, wet_bulb=20).magnitude,
            100,
        )
        < 0.01
    )
    assert (
        abs_relative_error(
            humidity_from_wetbulb_and_drybulb(temperature=30, wet_bulb=20).magnitude,
            38.957,
        )
        < 0.01
    )
    assert (
        abs_relative_error(
            humidity_from_wetbulb_and_drybulb(temperature=20, wet_bulb=15).magnitude,
            58.376,
        )
        < 0.01
    )
