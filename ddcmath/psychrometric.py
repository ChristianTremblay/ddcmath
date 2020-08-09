#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from __future__ import division
import math

from ddcmath.temperature import c2f, f2c

# Thanks Joel Bender for the formulae
def enthalpy(oat=None, rh=None, SI=True):
    if rh < 0 or rh > 100:
        raise ValueError("rh must be between 0-100%")
    if SI:
        oat = c2f(oat)
    return 0.24 * oat + 0.0010242 * rh * (2.7182818 ** (oat / 28.116)) * (
        13.147 + 0.0055 * oat
    )


def dewpoint(temp, hum, SI=True):
    if not SI:
        temp = f2c(temp)

    n = (math.log(hum / 100) + ((17.27 * temp) / (237.3 + temp))) / 17.27

    d = (237.3 * n) / (1 - n)
    if not SI:
        return c2f(d)
    else:
        return d
