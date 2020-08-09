from ddcmath.psychrometric import enthalpy, dewpoint


def test_enthalpy():
    pass


def test_dewpoint():
    assert (dewpoint(temp=20, hum=60, SI=True) - 12) < 0.01
    assert (dewpoint(temp=40, hum=65, SI=False) - 29.22) < 0.01
