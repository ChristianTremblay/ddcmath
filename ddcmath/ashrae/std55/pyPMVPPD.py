#!python
# -*- coding: utf-8 -*-
"""
File : pyPMVPPD.py
ASHRAE Standard 55-2013
Normative Appendix B

Computer program for calculation of PMV-PPD
PMV : Predicted Mean Vote
PPD : Predicted Percentage of dissatisfaction

This is a work in progress to implement the feature presented in 
standard 55 in Python. I start by doing a simple copy of the algorithm
presented in the standard and I'll implement a more pythonic way after.

"""


from math import exp, sqrt


def fnps(TA):
    return exp(16.6536 - 4030.183 / (TA + 235))


class PMVPPD:
    """
    This class is used to compute PMV and PPD based on 
    clothing, MET, WME, air temperature, radiant mean temperature, air velocity, relative humidity
    """

    def __init__(self, CLO, MET, WME, TA, TR, VEL, RH, PA):
        """
        Initialization of object
        """
        if PA == 0:
            self.PA = RH * 10 * (fnps(TA))  # Water Vapor pressure
        else:
            self.PA = PA
        self.CLO = CLO  # Clothing (clo)
        self.MET = MET  # Metabolic Rate (met)
        self.WME = WME  # External Work, normally around 0 (met)
        self.TA = TA  # Air temperature (degC)
        self.TR = TR  # Mean radiant temperature (degC)
        self.VEL = VEL  # Relative air velocity (m/s)
        self.RH = RH  # Relative humidity (%rh)
        self.ICL = 0.155 * self.CLO  # Thermal insulation of the clothing in m^2K/W
        self.M = self.MET * 58.15  # Metabolic Rate (W/m^2)
        self.W = WME * 58.15  # External Work (W/m^2)
        self.MW = self.M - self.W  # Internal heat production in the human body
        self.error = False

        # Clothing Area factor
        if self.ICL < 0.078:
            self.FCL = 1 + (1.29 * self.ICL)
        else:
            self.FCL = 1.05 + (0.645 * self.ICL)
        self.HCF = 12.1 * sqrt(
            self.VEL
        )  # Heat transfer coefficient by forced convection
        self.TAA = self.TA + 273  # Ait temp in Kelvin
        self.TRA = self.TR + 273  # Mean radiant temp in Kelvin
        PMVPPD.getClothingSurfaceTemp(self)
        PMVPPD.calculatePMVandPPD(self)

    def getClothingSurfaceTemp(self):
        """
        This function compute Clothing surface temperature
        """
        # First guess
        self.TCLA = self.TAA + (35.5 - self.TA) / (3.5 * (6.45 * self.ICL + 0.1))
        P1 = self.ICL * self.FCL
        P2 = P1 * 3.96
        P3 = P1 * 100
        P4 = P1 * self.TAA
        P5 = 308.7 - 0.028 * self.MW + P2 * (self.TRA / 100) ** 4
        XN = self.TCLA / 100
        XF = XN
        N = 0
        self.HC = 0
        EPS = 0.00015
        X = 1
        while X > EPS:
            XF = (XF + XN) / 2
            self.HCN = 2.38 * abs(100 * XF - self.TAA) ** 0.25

            if self.HCF > self.HCN:
                self.HC = self.HCF
            else:
                self.HC = self.HCN

            XN = (P5 + P4 * self.HC - P2 * XF ** 4) / (100 + P3 * self.HC)
            print(
                "Iteration : %s ; Value of XN = %s ; abs(XN-XNF) %s"
                % (N, XN, abs(XN - XF))
            )
            N += 1
            if N > 150:
                print("Too much iterations")
                self.PMV = 99999
                self.PPD = 100
                self.error = True
                break
            X = abs(XN - XF)

        self.TCL = 100 * XN - 273

        # Heat loss component
        # Heat loss diff through skin
        self.HL1 = 3.05 * 0.001 * (5733 - 6.99 * self.MW - self.PA)
        # Heat loss by sweating (comfort)
        if self.MW > 58.15:
            self.HL2 = 0.42 * (self.MW - 58.15)
        else:
            self.HL2 = 0
        # Latent respiration heat loss
        self.HL3 = 1.7 * 0.00001 * self.M * (5867 - self.PA)
        # Dry respiration heat loss
        self.HL4 = 0.0014 * self.M * (34 - self.TA)
        # Heat loss by radiation
        self.HL5 = 3.96 * self.FCL * (XN ** 4 - (self.TRA / 100) ** 4)
        # Heat loss by convection
        self.HL6 = self.FCL * self.HC * (self.TCL - self.TA)

    def calculatePMVandPPD(self):
        """
        This module compute PMV and PPD
        """
        if not self.error:
            # Thermal sensation trans. coeff.
            self.TS = 0.303 * exp(-0.036 * self.M) + 0.028
            # Predicted Mean vote
            self.PMV = self.TS * (
                self.MW
                - self.HL1
                - self.HL2
                - self.HL3
                - self.HL4
                - self.HL5
                - self.HL6
            )
            # Predicted percentage dissastisfaction
            self.PPD = 100 - 95 * exp(-0.03353 * self.PMV ** 4 - 0.2179 * self.PMV ** 2)

        return "PMV : %s \n PPD : %s" % (self.PMV, self.PPD)

    def getPMV(self):
        """
        Getter for PMV
        """
        return self.PMV

    def getPPD(self):
        """
        Getter for PPD
        """
        return self.PPD
