#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from __future__ import division

from ddcmath.temperature import f2c, c2f, delta_c2f, delta_f2c, oat_percent, mkt
from ddcmath.tolerance import abs_relative_error
from ddcmath.exceptions import InaccuracyException

import pytest

try:
    import numpy as np
    import pandas as pd
    PERM_MKT = True
except ImportError:
    PERM_MKT = False

def test_f2c():
    """
    Error must be lower than 0.001%
    """
    assert abs_relative_error(f2c(32), 0) < 0.001
    assert abs_relative_error(f2c(-40), -40) < 0.001
    
def test_c2f():
    """
    Error must be lower than 0.001%
    """
    assert abs_relative_error(c2f(0), 32) < 0.001
    assert abs_relative_error(c2f(-40),-40) < 0.001
    
def test_delta_c2f():
    assert delta_c2f(1) == 9/5
    
def test_delta_f2c():
    assert delta_f2c(1) == 5/9


def test_oa_proportion():
    assert oat_percent(0,20,10) == 0.5
    
def test_inaccuracy_of_oa_prop():
    with pytest.raises(InaccuracyException):
        oat_percent(20.000001,20,10) == 0.5

def test_mkt():
    if not PERM_MKT:
        return True
    records = [19.8,20.2,20.6,21,21.3,21.5]
    start = pd.datetime(2018, 9, 11,0,0)
    end = pd.datetime(2018, 9, 11,0,5)
    index = pd.date_range(start, end, freq='1Min')
    rec = pd.Series(records, index=index)
    rec2 = pd.Series(records)
    assert abs_relative_error(mkt(rec),20.752780387897474) < 0.001
    assert abs_relative_error(mkt(rec2),20.752780387897474) < 0.001