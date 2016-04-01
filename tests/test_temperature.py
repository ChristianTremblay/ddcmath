#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from ddcmath.temperature import f2c, c2f, delta_c2f, delta_f2c, oat_percent

def test_f2c():
    assert abs(f2c(32) - 0) < 0.0001
    assert abs(f2c(-40) + 40) < 0.0001
    
def test_c2f():
    assert abs(c2f(0) - 32) < 0.0001
    assert abs(c2f(-40) + 40) < 0.0001