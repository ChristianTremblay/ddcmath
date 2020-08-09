#!python
# -*- coding: utf-8 -*-
"""
File : findSET.py
ASHRAE Standard 55-2013
Normative Appendix G1

Computer program for calculation of SET

"""
from math import exp, pow


class SET:
    def __init__(self, TA, TR, VEL, RH, MET, CLO, WME, PATM):
        self.KCLO = 0.25
        self.BODYWEIGHT = 69.9
        self.BODYSURFACEAREA = 1.8258
        self.METFACTOR = 58.2
        self.SBC = 0.000000056697
        self.CSW = 170.0
        self.CDIL = 120.0
        self.CSTR = 0.5
        self.LTIME = 60
        self.VaporPressure = RH * findSaturatedVaporPressureTorr(TA) / 100
        self.AirVelocity = max(VEL, 0.1)
        self.tempSkinNeutral = 33.7
        self.tempCoreNeutral = 36.49
        self.tempBodyNeutral = 36.49
        self.skinBloodFlowNeutral = 6.3
        self.tempSkin = self.tempSkinNeutral
        self.tempCore = self.tempCoreNeutral
        self.skinBloodFlow = self.skinBloodFlowNeutral
        self.MSHIV = 0.0
        self.ALFA = 0.1
        self.ESK = 0.1 * MET
        self.pressureATM = PATM * 0.009869
        self.RCL = 0.155 * CLO
        self.FACL = 1.0 + 0.15 * CLO
        self.LR = 2.2 / self.pressureATM
        self.RM = MET * self.METFACTOR
        self.M = MET * self.METFACTOR
        if CLO <= 0:
            self.WCRIT = 0.38 * pow(self.AirVelocity, -0.29)
            self.ICL = 1
        else:
            self.WCRIT = 0.59 * pow(self.AirVelocity, -0.08)
            self.ICL = 0.45

        self.CHC = 3.0 * pow(self.pressureATM, 0.53)
        self.CHCV = 8.600001 * pow((self.AirVelocity * self.pressureATM), 0.53)
        self.CHC = max(self.CHC, self.CHCV)
        self.CHR = 4.7
        self.CTC = self.CHR + self.CHC
        self.RA = 1.0 / (self.FACL * self.CTC)
        self.TOP = (self.CHR * TR + self.CHC * TA) / self.CTC
        self.TCL = self.TOP + (self.tempSkin - self.TOP) / (
            self.CTC * (self.RA + self.RCL)
        )
        self.TCL_OLD = self.TCL
        self.flag = True
        self.var = {
            "DRY": 0,
            "HFCS": 0,
            "ERES": 0,
            "CRES": 0,
            "SCR": 0,
            "SSK": 0,
            "TCSK": 0,
            "TCCR": 0,
            "DTSK": 0,
            "DTCR": 0,
            "TB": 0,
            "SKSIG": 0,
            "WARMS": 0,
            "COLDS": 0,
            "CRSIG": 0,
            "WARMC": 0,
            "COLDC": 0,
            "BDSIG": 0,
            "WARMB": 0,
            "COLDB": 0,
            "REGSW": 0,
            "ERSW": 0,
            "REA": 0,
            "RECL": 0,
            "EMAX": 0,
            "PRSW": 0,
            "PWET": 0,
            "EDIF": 0,
            "ESK": 0,
        }

        print("Begin iteration | TCL : %s " % (self.TCL))
        for each in range(0, self.LTIME):
            while self.flag:
                # print 'Condition : %s' % abs(self.TCL - self.TCL_OLD)
                self.TCL_OLD = self.TCL
                self.CHR = (
                    4.0 * self.SBC * pow(((self.TCL + TR) / 2.0 + 273.15), 3.0) * 0.72
                )
                self.CTC = self.CHR + self.CHC
                self.RA = 1.0 / (self.FACL * self.CTC)
                self.TOP = (self.CHR * TR + self.CHC * TA) / self.CTC
                self.TCL = (self.RA * self.tempSkin + self.RCL * self.TOP) / (
                    self.RA + self.RCL
                )
                self.flag = abs(self.TCL - self.TCL_OLD) > 0.01
                # print 'Flag is : %s | TCL = %s | TCL_OLD = %s' % (self.flag,self.TCL,self.TCL_OLD)

            self.var["DRY"] = (self.tempSkin - self.TOP) / (self.RA + self.RCL)
            self.var["HFCS"] = (self.tempCore - self.tempSkin) * (
                5.28 + 1.163 * self.skinBloodFlow
            )
            self.var["ERES"] = 0.0023 * self.M * (44.0 - self.VaporPressure)
            self.var["CRES"] = 0.0014 * self.M * (34.0 - TA)
            self.var["SCR"] = (
                self.M - self.var["HFCS"] - self.var["ERES"] - self.var["CRES"] - WME
            )
            self.var["SSK"] = self.var["HFCS"] - self.var["DRY"] - self.ESK
            self.var["TCSK"] = 0.97 * self.ALFA * self.BODYWEIGHT
            self.var["TCCR"] = 0.97 * (1 - self.ALFA) * self.BODYWEIGHT
            self.var["DTSK"] = (self.var["SSK"] * self.BODYSURFACEAREA) / (
                self.var["TCSK"] * 60.0
            )  # degC/min
            self.var["DTCR"] = (self.var["SCR"] * self.BODYSURFACEAREA) / (
                self.var["TCCR"] * 60.0
            )  # degC/min
            self.tempSkin += self.var["DTSK"]
            self.tempCore += self.var["DTCR"]
            self.var["TB"] = self.ALFA * self.tempSkin + (1 - self.ALFA) * self.tempCore
            self.var["SKSIG"] = self.tempSkin - self.tempSkinNeutral
            self.var["WARMS"] = (self.var["SKSIG"] > 0) * self.var["SKSIG"]
            # print 'SKSIG : %s | WARMS : %s' % (self.var['SKSIG'], self.var['WARMS'])
            # print '(self.var["SKSIG"]>0) : %s' % ((self.var['SKSIG']>0)* self.var['SKSIG'])
            self.var["COLDS"] = ((-1.0 * self.var["SKSIG"]) > 0) * (
                -1.0 * self.var["SKSIG"]
            )
            self.var["CRSIG"] = self.tempCore - self.tempCoreNeutral
            self.var["WARMC"] = (self.var["CRSIG"] > 0) * self.var["CRSIG"]
            self.var["COLDC"] = ((-1.0 * self.var["CRSIG"]) > 0) * (
                -1.0 * self.var["CRSIG"]
            )
            self.var["BDSIG"] = self.var["TB"] - self.tempBodyNeutral
            self.var["WARMB"] = (self.var["BDSIG"] > 0) * self.var["BDSIG"]
            self.skinBloodFlow = (
                self.skinBloodFlowNeutral + self.CDIL * self.var["WARMC"]
            ) / (1 + self.CSTR * self.var["COLDS"])
            self.skinBloodFlow = max(0.5, min(90, self.skinBloodFlow))
            self.var["REGSW"] = (
                self.CSW * self.var["WARMB"] * exp(self.var["WARMS"] / 10.7)
            )
            self.var["REGSW"] = min(self.var["REGSW"], 500)
            self.var["ERSW"] = 0.68 * self.var["REGSW"]
            self.var["REA"] = 1.0 / (self.LR * self.FACL * self.CHC)
            self.var["RECL"] = self.RCL / (self.LR * self.ICL)
            self.var["EMAX"] = (
                findSaturatedVaporPressureTorr(self.tempSkin) - self.VaporPressure
            ) / (self.var["REA"] + self.var["RECL"])
            self.var["PRSW"] = self.var["ERSW"] / self.var["EMAX"]
            self.var["PWET"] = 0.06 + 0.94 * self.var["PRSW"]
            self.var["EDIF"] = self.var["PWET"] * self.var["EMAX"] - self.var["ERSW"]
            self.ESK = self.var["ERSW"] + self.var["EDIF"]

            if self.var["PWET"] > self.WCRIT:
                self.var["PWET"] = self.WCRIT
                self.var["PRSW"] = self.WCRIT / 0.94
                self.var["ERSW"] = self.var["PRSW"] * self.var["EMAX"]
                self.var["EDIF"] = 0.06 * (1.0 - self.var["PRSW"]) * self.var["EMAX"]
                self.ESK = self.var["ERSW"] + self.var["EDIF"]

            if self.var["EMAX"] < 0:
                self.var["EDIF"] = 0
                self.var["ERSW"] = 0
                self.var["PWET"] = self.WCRIT
                self.var["PRSW"] = self.WCRIT
                self.ESK = self.var["EMAX"]

            self.ESK = self.var["ERSW"] + self.var["EDIF"]
            self.MSHIV = 19.4 * self.var["COLDS"] * self.var["COLDC"]
            self.M = self.RM + self.MSHIV
            self.ALFA = 0.0417737 + 0.7451833 / (self.skinBloodFlow + 0.585417)
        # End FOR LOOP
        print("Iteration over...")
        self.HSK = self.var["DRY"] + self.ESK
        self.RN = self.M - WME
        self.ECOMF = 0.42 * (self.RN - (1 * self.METFACTOR))
        if self.ECOMF < 0:
            self.ECOMF = 0
        self.var["EMAX"] = self.var["EMAX"] * self.WCRIT
        self.W = self.var["PWET"]
        self.PSSK = findSaturatedVaporPressureTorr(self.tempSkin)
        self.CHRS = self.CHR

        if MET < 0.85:
            self.CHCS = 3.0
        else:
            self.CHCS = 5.66 * pow((MET - 0.85), 0.39)
            self.CHCS = max(self.CHCS, 3.0)

        self.CTCS = self.CHCS + self.CHRS
        self.RCLOS = 1.52 / ((MET - WME / self.METFACTOR) + 0.6944) - 0.1835
        self.RCLS = 0.155 * self.RCLOS
        self.FACLS = 1.0 + self.KCLO * self.RCLOS
        self.FCLS = 1.0 / (1.0 + 0.155 * self.FACLS * self.CTCS * self.RCLOS)
        self.IMS = 0.45
        self.ICLS = (
            self.IMS
            * self.CHCS
            / self.CTCS
            * (1 - self.FCLS)
            / (self.CHCS / self.CTCS - self.FCLS * self.IMS)
        )
        self.RAS = 1.0 / (self.FACLS * self.CTCS)
        self.REAS = 1.0 / (self.LR * self.FACLS * self.CHCS)
        self.RECLS = self.RCLS / (self.LR * self.ICLS)
        self.HD_S = 1.0 / (self.RAS + self.RCLS)
        self.HE_S = 1.0 / (self.REAS + self.RECLS)

        # SET determined using Newton's iterative solution
        self.DELTA = 0.0001
        self.dx = 100
        self.result = {"SET": 0, "ERR1": 0, "ERR2": 0}
        self.SET_OLD = self.tempSkin - self.HSK / self.HD_S
        print("Finding SET with Newton iterative solution")
        while abs(self.dx) > 0.01:
            self.result["ERR1"] = (
                self.HSK
                - self.HD_S * (self.tempSkin - self.SET_OLD)
                - self.W
                * self.HE_S
                * (self.PSSK - 0.5 * findSaturatedVaporPressureTorr(self.SET_OLD))
            )
            self.result["ERR2"] = (
                self.HSK
                - self.HD_S * (self.tempSkin - (self.SET_OLD + self.DELTA))
                - self.W
                * self.HE_S
                * (
                    self.PSSK
                    - 0.5 * findSaturatedVaporPressureTorr(self.SET_OLD + self.DELTA)
                )
            )
            self.result["SET"] = self.SET_OLD - self.DELTA * self.result["ERR1"] / (
                self.result["ERR2"] - self.result["ERR1"]
            )
            self.dx = self.result["SET"] - self.SET_OLD
            self.SET_OLD = self.result["SET"]

        print("Done... SET : %s" % self.result["SET"])

    def getSET(self):
        return self.result["SET"]


def findSaturatedVaporPressureTorr(temp):
    """
        Helper function for SET. Calculates Saturated Vapor pressure (Torr) at temperature 'temp' (degC)
        """
    return exp(18.6686 - 4030.183 / (temp + 235))
