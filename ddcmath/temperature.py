#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.

def oat_percent(oat, mat, rat):
    """
    Returns outdoor air proportion based on outside air temp, mixed air
    temp and return air temp on a rooftop unit
    
    :params: mat (mixed air temp)
    :params: oat (outdoor air temp)
    :params: rat (return air temp)
    
    :returns: oat_prop (outdoor air proportion in %)
    """
    prop_oat = (mat - rat) / (oat - rat)
    return prop_oat
    
def f2c(temp_in_farenheit = None):
    """
    Convert farenheit to celsius
    """
    return (temp_in_farenheit - 32) * 5.0/9.0
    
def c2f(temp_in_celsius = None):
    """
    Convert farenheit to celsius
    """
    return (temp_in_celsius * 9.0/5.0) + 32
    
def delta_c2f(delta_t_celsius = None):
    return delta_t_celsius * (9.0/5.0)
    
def delta_f2c(delta_t_farenheit = None):
    return delta_t_farenheit * (5.0/9.0)