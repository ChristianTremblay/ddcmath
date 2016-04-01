#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from ddcmath.heating import heating_cfm, heating_ls, heating_kw

def test_heating_cfm():
    assert abs(heating_cfm(kw = 1, delta_t_farenheit = 3.15926) - 1000) < 0.25
    assert abs(heating_cfm(kw = 1, delta_t_celsius = 1.7551) - 1000) < 0.25
    
def test_heating_ls():
    assert abs(heating_ls(kw = 1, delta_t_farenheit = 3.15926) - 471.843) < 0.25
    assert abs(heating_ls(kw = 1, delta_t_celsius = 1.7551) - 471.843) < 0.25
    
def test_heating_kw():
    assert abs(heating_kw(cfm = 1000, delta_t_farenheit = 3.16) - 1) < 0.001