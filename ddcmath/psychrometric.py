#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from __future__ import division
import math
import pint

from ddcmath.temperature import c2f, f2c


ureg = pint.UnitRegistry()
ureg.define(
    pint.unit.UnitDefinition("percent", "%", (), pint.converters.ScaleConverter(0.01))
)
ureg.default_format = ".2f"
Q_ = ureg.Quantity


def enthalpy(temperature=None, humidity=None, wet_bulb=None, SI=True):
    """
    Result in BTU/lb

    Greatly inspired by
    https://www.mrexcel.com/board/threads/excel-formula-for-calculating-airs-enthalpy-from-dry-bulb-temperature-and-relative-humidity.871843/

    This formulae use Imperial Units
    """
    temperature = validate_temperature(temperature, SI=SI)
    wet_bulb = validate_temperature(wet_bulb, SI=SI)
    humidity = validate_humidity(humidity, SI=SI)

    rh = humidity.magnitude if humidity is not None else None
    Td = temperature.to("degF").magnitude
    Tw = wet_bulb.to("degF").magnitude if wet_bulb is not None else None
    if rh is None:
        if Tw and Td:
            rh = humidity_from_wetbulb_and_drybulb(Td, Tw, SI=False)
            rh = 100 if rh > 100 else rh
            rh = 0 if rh < 0 else rh
    if rh < 0 or rh > 100:
        raise ValueError("rh must be between 0-100%, actual result is {}".format(rh))

    # This one provided by Joel Bender is simpler and quite precise also
    # btu_lb =  (0.24 * Td) + ((0.0010242 * rh) * (2.7182818 ** (Td / 28.116)) * (13.147 + 0.0055 * Td ))

    # Metric conversion
    # kJ_kg = btu_lb * 2.326

    btu_lb = 0.24 * Td + (0.6219) * (
        0.01
        * (
            0.000000007401234 * Td ** 4
            - 0.000000493526794 * Td ** 3
            + 0.000071281097208 * Td ** 2
            - 0.000489806163078 * Td
            + 0.039762055806989
        )
        * rh
    ) / (
        14.7
        - (
            0.01
            * (
                0.000000007401234 * Td ** 4
                - 0.000000493526794 * Td ** 3
                + 0.000071281097208 * Td ** 2
                - 0.000489806163078 * Td
                + 0.039762055806989
            )
            * rh
        )
    ) * (
        1061.2 + 0.444 * Td
    )
    # kJ_kg = btu_lb * 2.326
    if SI:
        return Q_(btu_lb * 2.326, ureg.kJ / ureg.kg)
    else:
        return Q_(btu_lb, ureg.BTU / ureg.lb)


def dewpoint_from_temperature_and_humidity(temperature, humidity, SI=True):
    """
    This formula use SI units
    """
    print(temperature, humidity)
    temperature = validate_temperature(temperature, SI=SI)
    humidity = validate_humidity(humidity)
    print(temperature, humidity)
    temp = temperature.to("degC").magnitude
    hum = humidity.magnitude
    n = (math.log(hum / 100) + ((17.27 * temp) / (237.3 + temp))) / 17.27

    d = (237.3 * n) / (1 - n)
    dewpoint = Q_(d, ureg.degC)
    if SI:
        return dewpoint
    else:
        return dewpoint.to("degF")


def temperature_from_humidity_and_dewpoint(dewpoint, humidity, SI=True):
    """
    This formula use SI units
    """
    dewpoint = validate_temperature(dewpoint, SI=SI)
    humidity = validate_humidity(humidity, SI=SI)

    C = 243.04
    D = 17.625
    TD = dewpoint.to("degC").magnitude
    RH = humidity.magnitude
    t = (
        C
        * (((D * TD) / (C + TD)) - math.log(RH / 100))
        / (D + math.log(RH / 100) - ((D * TD) / (C + TD)))
    )
    temperature = Q_(t, ureg.degC)
    if SI:
        return temperature
    else:
        return temperature.to("degF")


def humidity_from_wetbulb_and_drybulb(temperature, wet_bulb, SI=True):
    """
    Ref : http://www.1728.org/relhum.htm
    Metric system only
    """
    temperature = validate_temperature(temperature, SI=SI)
    wet_bulb = validate_temperature(wet_bulb, SI=SI)

    Td = temperature.to("degC").magnitude
    Tw = wet_bulb.to("degC").magnitude

    N = 0.6687451584
    ed = 6.112 * math.exp((17.502 * Td) / (240.97 + Td))
    ew = 6.112 * math.exp((17.502 * Tw) / (240.97 + Tw))

    hum = ((ew - (N * (1 + 0.00115 * Tw) * (Td - Tw))) / ed) * 100
    humidity = Q_(hum, ureg.percent)
    return humidity


def wetbulb_from_humidity_and_temperature(humidity, temperature, SI=True):
    """
    This one is and estimate as explained here :
    https://journals.ametsoc.org/view/journals/apme/50/11/jamc-d-11-0143.1.xml

    SI Units
    """
    temperature = validate_temperature(temperature, SI=SI)
    humidity = validate_humidity(humidity, SI=SI)

    Td = temperature.to("degC").magnitude
    rh = humidity.magnitude

    wb = (
        Td * math.atan(0.151977 * (rh + 8.313659) ** 0.5)
        + math.atan(Td + rh)
        - math.atan(rh - 1.676331)
        + 0.00391838 * (rh) ** (3 / 2) * math.atan(0.023101 * rh)
        - 4.686035
    )
    wetbulb = Q_(wb, ureg.degC)
    if SI:
        return wetbulb
    else:
        return wetbulb.to("degF")


def humidity_from_dewpoint_and_temperature(dewpoint, temperature, SI=True):
    """
    https://en.wikipedia.org/wiki/Dew_point
    Magnus Formula
    """
    print(dewpoint, temperature)
    dewpoint = validate_temperature(dewpoint, SI=SI)
    temperature = validate_temperature(temperature, SI=SI)
    print(dewpoint, temperature)
    Td = temperature.to("degC").magnitude
    dp = dewpoint.to("degC").magnitude

    c = 243.5
    b = 17.67
    a = (dp * b) / (c + dp)
    hum = math.exp(a - ((b * Td / (c + Td)))) * 100

    humidity = Q_(hum, ureg.percent)
    return humidity


class Psychrometric:
    """
    Get psychrometric info from one temperature and humidity or wet bulb temperature
    Pint is required
    Some results are approximations
    """

    SI = True

    @staticmethod
    def has_unit(value):
        try:
            value.dimensioanlity
            return True
        except AttributeError:
            return False

    def __init__(
        self, temperature=None, humidity=None, wetbulb=None, dewpoint=None, SI=True
    ):
        self.SI = SI
        if not temperature:
            raise ValueError("Dry buld temperature is required.")
        self.temperature = validate_temperature(temperature, SI=self.SI)
        self.wetbulb = validate_temperature(wetbulb, SI=self.SI)
        self.dewpoint = validate_temperature(dewpoint, SI=self.SI)
        if humidity is not None:
            self.humidity = validate_humidity(humidity)
            self.dewpoint = dewpoint_from_temperature_and_humidity(
                self.temperature, self.humidity, SI=self.SI
            )
            self.wetbulb = wetbulb_from_humidity_and_temperature(
                self.humidity, self.temperature, SI=self.SI
            )

        else:
            if wetbulb is None and wetbulb is None and dewpoint is None:
                raise ValueError("Please provide humidity or wetbulb or dewpoint")
            if wetbulb and dewpoint:
                ...  # need to validate that 2 numbers are correct

            elif wetbulb:
                self.humidity = humidity_from_wetbulb_and_drybulb(
                    self.temperature, self.wetbulb
                )
                self.dewpoint = dewpoint_from_temperature_and_humidity(
                    self.temperature, self.humidity, SI=self.SI
                )
            elif dewpoint:
                self.humidity = humidity_from_dewpoint_and_temperature(
                    self.dewpoint, self.temperature
                )
                self.wetbulb = wetbulb_from_humidity_and_temperature(
                    self.humidity, self.temperature, SI=self.SI
                )

        self.enthalpy = enthalpy(
            temperature=self.temperature, humidity=self.humidity, SI=self.SI
        )

    def __repr__(self):
        return "T: {} | H: {} | DP: {} | WET: {} -> Enthalpy: {}".format(
            self.temperature, self.humidity, self.dewpoint, self.wetbulb, self.enthalpy
        )


def validate_temperature(value, SI=True):
    if value is None:
        return value
    try:
        value.dimensionality
        if SI:
            if value.units == ureg.degC:
                return value
            elif value.units == ureg.degF:
                return value.to("degC")
            else:
                raise ValueError("Wrong units for temperature, should be degF")
        else:
            if value.units == ureg.degF:
                return value
            elif value.units == ureg.degC:
                return value.to("degF")
            else:
                raise ValueError("Wrong units for temperature, should be degC")
    except AttributeError:
        if SI:
            return Q_(value, ureg.degC)
        else:
            return Q_(value, ureg.degF)


def validate_humidity(value, SI=True):
    try:
        value.dimensionality
        if value.units == ureg.percent:
            value = value.magnitude
        else:
            raise ValueError("Wrong units for humidity, should be percent")
    except AttributeError:
        pass
    value = 0 if value < 0 else value
    value = 100 if value > 100 else value
    return Q_(value, ureg.percent)
