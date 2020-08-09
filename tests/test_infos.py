#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.

from ddcmath import infos


def test_infos():
    """
    I hate to see 0% coverage :-)
    """
    assert infos.__version__
    assert infos.__author__
    assert infos.__email__
    assert infos.__url__
    assert infos.__download_url__
    assert infos.__license__
