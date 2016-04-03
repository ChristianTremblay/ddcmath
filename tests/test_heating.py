#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.
from ddcmath.heating import heating_cfm, heating_ls, heating_kw
from ddcmath.airflow import cfm2ls
from ddcmath.tolerance import abs_relative_error

import pytest

def test_heating_cfm_farenheit():
    assert abs_relative_error(heating_cfm(kw = 1, delta_t_farenheit = 3.15926), 1000) < 0.003

def test_heating_cfm_celsius():
    assert abs_relative_error(heating_cfm(kw = 1, delta_t_celsius = 1.7551), 1000) < 0.003

def test_heating_cfm_too_much_params():
    with pytest.raises(ValueError):
        heating_cfm(kw = 1, delta_t_celsius = 1.7551, delta_t_farenheit = 3.15926)

def test_missing_params():
    with pytest.raises(ValueError):
        heating_cfm(delta_t_farenheit = 3.15926)
    with pytest.raises(ValueError):
        heating_cfm(kw = None, delta_t_farenheit = 3.15926)
    with pytest.raises(ValueError):
        heating_cfm(kw = None)
    with pytest.raises(ValueError):
        heating_cfm(kw = None, delta_t_farenheit = None)
    with pytest.raises(ValueError):
        heating_cfm(kw = None, delta_t_celsius = None)
        
def test_param_0():
    with pytest.raises(ValueError):
        heating_cfm(kw = 1, delta_t_farenheit = 0)
    with pytest.raises(ValueError):
        heating_cfm(kw = 1, delta_t_celsius = 0)
    with pytest.raises(ValueError):
        heating_cfm(kw = 0, delta_t_farenheit = 2)
    with pytest.raises(ValueError):
        heating_cfm(kw = 0, delta_t_celsius = 2)
    
   
def test_heating_ls_farenheit():
    assert abs_relative_error(heating_ls(kw = 1, delta_t_farenheit = 3.15926), cfm2ls(1000)) < 0.003

def test_heating_ls_celsius():
    assert abs_relative_error(heating_ls(kw = 1, delta_t_celsius = 1.7551), cfm2ls(1000)) < 0.003
    
def test_heating_kw_cfm_farenheit():
    assert abs_relative_error(heating_kw(cfm = 1000, delta_t_farenheit = 3.15926), 1) < 0.003

def test_heating_kw_cfm_celsius():
    assert abs_relative_error(heating_kw(cfm = 1000, delta_t_celsius = 1.7551), 1) < 0.003

def test_heating_kw_ls_farenheit():
    assert abs_relative_error(heating_kw(ls = cfm2ls(1000), delta_t_farenheit = 3.15926), 1) < 0.003

def test_heating_kw_ls_celsius():
    assert abs_relative_error(heating_kw(ls = cfm2ls(1000), delta_t_celsius = 1.7551), 1) < 0.003

    
def test_heating_kw_missing_params():
    with pytest.raises(ValueError):
        heating_kw(cfm = None, delta_t_farenheit = 3.15926)
    with pytest.raises(ValueError):
        heating_kw(delta_t_farenheit = 3.15926)
    