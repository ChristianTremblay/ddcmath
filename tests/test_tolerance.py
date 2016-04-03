#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.

from ddcmath.tolerance import relative_error, abs_relative_error

def test_relative_error():
    result = 9
    answer = 10
    assert relative_error(result,answer) == -10
    
def test_abs_relative_error():
    result = 9
    answer = 10
    assert abs_relative_error(result,answer) == 10