#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from __future__ import division

from .exceptions import InaccuracyException

try:
    import numpy as np
    import pandas as pd

    PERM_MKT = True
except ImportError:
    PERM_MKT = False


def oat_percent(oat, rat, mat):
    """
    Returns outdoor air proportion based on outside air temp, mixed air
    temp and return air temp on a rooftop unit
    
    :params: mat (mixed air temp)
    :params: oat (outdoor air temp)
    :params: rat (return air temp)
    
    :returns: oat_prop (outdoor air proportion in %)
    """
    if oat >= 20:
        raise InaccuracyException(
            "Outside air temperature too high. Will lead to wrong result"
        )
    prop_oat = (mat - rat) / (oat - rat)
    return prop_oat


def f2c(temp_in_farenheit=None):
    """
    Convert farenheit to celsius
    """
    return (temp_in_farenheit - 32) * 5.0 / 9.0


def c2f(temp_in_celsius=None):
    """
    Convert farenheit to celsius
    """
    return (temp_in_celsius * 9.0 / 5.0) + 32


def delta_c2f(delta_t_celsius=None):
    return delta_t_celsius * (9.0 / 5.0)


def delta_f2c(delta_t_farenheit=None):
    return delta_t_farenheit * (5.0 / 9.0)


def mkt(temp_serie, delta_H=83.14472, gas_constant=0.008314472, units="SI"):
    """
    Mean Kinetic Temperature
    [ref : https://en.wikipedia.org/wiki/Mean_kinetic_temperature]
    If serie is provided as a time serie, formulae will consider time delta between
    records. If not, simple mean will be used.
    """
    k_constant = 273.15
    delta_H = delta_H  # kJ/mole
    gas_constant = gas_constant  # kJ/mole/degree
    df = pd.DataFrame({"values": temp_serie})
    if "SI" not in units:
        df["values"] = df["values"].apply(lambda x: f2c(x))
    df["kelvin"] = df["values"] + k_constant

    if isinstance(df.index, pd.DatetimeIndex):
        df["delta_T"] = df.index.to_series().diff().bfill().dt.total_seconds()
        df["denominator"] = df.apply(
            lambda x: x["delta_T"] * np.exp(-delta_H / (gas_constant * x["kelvin"])),
            axis=1,
        )
        ln = np.log(df["denominator"].sum() / (df["delta_T"].sum())) * -1
    else:
        df["denominator"] = df.apply(
            lambda x: np.exp(-delta_H / (gas_constant * x["kelvin"])), axis=1
        )
        ln = np.log(df["denominator"].mean()) * -1
    numerator = delta_H / gas_constant
    res = (numerator / ln) - k_constant
    return res
