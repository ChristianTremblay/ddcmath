#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from ddcmath.airflow import cfm2ls, ls2cfm


def test_cfm2ls():
    assert cfm2ls(1) == 0.4719475


def test_ls2cfm():
    assert ls2cfm(1) == 2.118879748277086
    assert ls2cfm((cfm2ls(1))) == 1
