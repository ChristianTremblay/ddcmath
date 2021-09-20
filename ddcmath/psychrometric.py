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
ureg.define(pint.unit.UnitDefinition('percent', '%', (),
            pint.converters.ScaleConverter(0.01)))
ureg.default_format = '.2f'
Q_ = ureg.Quantity



# Thanks Joel Bender for the formulae
def enthalpy(Td=None, rh=None, Tw=None, SI=True):
    """
    Result in BTU/lb

    This formulae use Imperial Units
    """
    Td = validate_temperature(Td, SI=False)
    Tw = validate_temperature(Tw, SI=False)
    rh = validate_humidity(rh, SI=False)
    if rh is None:
        if Tw and Td:
            if not SI:
                Td = f2c(Td)
                Tw = f2c(Tw)
            rh = humidity_from_wetbulb_and_drybulb(Td, Tw)
            rh = 100 if rh > 100 else rh
            rh = 0 if rh < 0 else rh
    if rh < 0 or rh > 100:
        raise ValueError("rh must be between 0-100%, actual result is {}".format(rh))
    if SI:
        Td = c2f(Td)
    #btu_lb =  (0.24 * Td) + ((0.0010242 * rh) * (2.7182818 ** (Td / 28.116)) * (13.147 + 0.0055 * Td ))
    #kJ_kg = btu_lb * 2.326
    #kJ_kg = 0.24*Td+(597.3+0.441*Td)*0.622*(10^(8.10765-1750.29/(Td+235))*rh/100)/(760-(10^(8.10765-1750.29/(Td+235))*rh/100))
    btu_lb = 0.24*Td+(0.6219)*(0.01*(0.000000007401234*Td**4 - 0.000000493526794*Td**3 + 0.000071281097208*Td**2 - 0.000489806163078*Td + 0.039762055806989)*rh)/(14.7-(0.01*(0.000000007401234*Td**4 - 0.000000493526794*Td**3 + 0.000071281097208*Td**2 - 0.000489806163078*Td + 0.039762055806989)*rh))*(1061.2+0.444*Td)
    kJ_kg = btu_lb * 2.326
    if SI:
        return Q_(kJ_kg, ureg.kJ/ureg.kg)
    else:
        return Q_(btu_lb, ureg.BTU/ureg.lb)
    


def dewpoint_from_temperature_and_humidity(temp, hum):
    """
    This formula use SI units
    """
    temp = validate_temperature(temp, SI=True)
    hum = validate_humidity(hum)
    n = (math.log(hum / 100) + ((17.27 * temp) / (237.3 + temp))) / 17.27

    d = (237.3 * n) / (1 - n)
    return d

def temperature_from_humidity_and_dewpoint(dewpoint, humidity):
    C = 243.04
    D = 17.625
    TD = dewpoint
    RH = humidity
    return (
        C
        * (((D * TD) / (C + TD)) - math.log(RH / 100))
        / (D + math.log(RH / 100) - ((D * TD) / (C + TD)))
    )

def humidity_from_wetbulb_and_drybulb(Td, Tw):
    """
    Ref : http://www.1728.org/relhum.htm
    Metric system only
    """
    N = 0.6687451584
    ed = 6.112 * math.exp((17.502 * Td)/(240.97 + Td))
    ew = 6.112 * math.exp((17.502 * Tw)/(240.97 + Tw))

    hum = ((ew - (N * (1+0.00115*Tw)*(Td-Tw)))/ed)*100
    return hum

def wetbulb_from_humidity_and_temperature(rh, Td):
    """
    This one is an estimate as explained here : 
    https://journals.ametsoc.org/view/journals/apme/50/11/jamc-d-11-0143.1.xml
    """
    return Td*math.atan(0.151977*(rh + 8.313659)**0.5) + math.atan(Td + rh) - math.atan(rh - 1.676331) + 0.00391838*(rh)**(3/2) * math.atan(0.023101*rh) - 4.686035


def humidity_from_dewpoint_and_temperature(dp, Td):
    return math.exp((-17.67*Td)/(257.14+Td))*100

class Psychrometric():
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
        

    def __init__(self, temperature=None, humidity=None, wetbulb=None, dewpoint=None, SI=True):

        self.define_units(SI)
        if not temperature:
            raise ValueError('Dry buld temperature is required.')
        self.temperature = validate_temperature(temperature)
        if humidity is not None:
            self.humidity = humidity 
            self.dewpoint = dewpoint_from_temperature_and_humidity(self.temperature, self.humidity)
            self.wetbulb = wetbulb_from_humidity_and_temperature(self.humidity, self.temperature)

        else:
            if wetbulb is None and wetbulb is None:
                raise ValueError('Please provide humidity or wetbulb or dewpoint')
            if wetbulb and dewpoint:
                ... # need to validate that 2 numbers are correct

            elif wetbulb:
                self.wetbulb = wetbulb
                self.humidity = humidity_from_wetbulb_and_drybulb(self.temperature, self.wetbulb)
                self.dewpoint = dewpoint_from_temperature_and_humidity(self.temperature, self.humidity)
            elif dewpoint:
                self.dewpoint = dewpoint
                self.humidity = humidity_from_dewpoint_and_temperature(dewpoint, temperature)

        self.enthalpy = enthalpy(Td=self.temperature, rh=self.humidity)

    def __repr__(self):
        return "T: {} | H: {} | DP: {} | WET: {} -> Enthalpy: {}".format(self.temperature, self.humidity, self.dewpoint, self.wetbulb, self.enthalpy)


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
                raise ValueError('Wrong units for temperature, should be degF')
        else:
            if value.units == ureg.degF:
                return value
            elif value.units == ureg.degC:
                return value.to("degF")
            else:
                raise ValueError('Wrong units for temperature, should be degC')
    except AttributeError:
        if SI:
            return Q_(value, ureg.degC)
        else:
            return Q_(value, ureg.degF)

def validate_humidity(value):
    try:
        value.dimensionality
        if value.units == ureg.percent:
            return value
        else:
            raise ValueError('Wrong units for humidity, should be percent')
    except AttributeError:
        return Q_(value, ureg.percent)