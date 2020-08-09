"""
Created on Sep 7, 2014

@author: CTremblay
"""
import unittest

from ddcmath.ashrae.std55 import pyPMVPPD
from ddcmath.ashrae.std55 import pySET


class Test(unittest.TestCase):
    def testPMVPPD(self):
        """
        Test values based on Example p.18 of Standard, values used to generate comfort envelope in Figure 5.3.1
        """
        self.result = pyPMVPPD.PMVPPD(1, 1.1, 0, 19.6, 19.6, 0.1, 86, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), -0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 10, "Test PPD")

        self.result = pyPMVPPD.PMVPPD(1, 1.1, 0, 23.9, 23.9, 0.1, 66, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), 0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 10, "Test PPD")

        self.result = pyPMVPPD.PMVPPD(1, 1.1, 0, 25.7, 25.7, 0.1, 15, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), 0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 11, "Test PPD")

        self.result = pyPMVPPD.PMVPPD(1, 1.1, 0, 21.2, 21.2, 0.1, 20, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), -0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 10, "Test PPD")

        self.result = pyPMVPPD.PMVPPD(0.5, 1.1, 0, 23.6, 23.6, 0.1, 67, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), -0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 10, "Test PPD")

        self.result = pyPMVPPD.PMVPPD(0.5, 1.1, 0, 26.8, 26.8, 0.1, 56, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), 0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 11, "Test PPD")

        self.result = pyPMVPPD.PMVPPD(0.5, 1.1, 0, 27.9, 27.9, 0.1, 13, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), 0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 10, "Test PPD")

        self.result = pyPMVPPD.PMVPPD(0.5, 1.1, 0, 24.7, 24.7, 0.1, 16, 0)
        print(
            "PMV : %s \nPPD : %s"
            % (
                float("{0:.1f}".format(self.result.PMV)),
                float("{0:.0f}".format(self.result.PPD)),
            )
        )
        self.assertEqual(float("{0:.1f}".format(self.result.PMV)), -0.5, "Test PMV")
        self.assertEqual(float("{0:.0f}".format(self.result.PPD)), 10, "Test PPD")

    def testSET(self):
        """
        Testing based on Table G1-1 Validate SET Computer Model
        """
        # Build Table
        self.tableG1 = []
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 23.9,
            }
        )
        self.tableG1.append(
            {
                "TA": 0,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 12.4,
            }
        )
        self.tableG1.append(
            {
                "TA": 10,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 17,
            }
        )
        self.tableG1.append(
            {
                "TA": 15,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 19.3,
            }
        )
        self.tableG1.append(
            {
                "TA": 20,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 21.6,
            }
        )
        self.tableG1.append(
            {
                "TA": 30,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 26.2,
            }
        )
        self.tableG1.append(
            {
                "TA": 40,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 33.6,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 10,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 23.3,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 90,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 24.4,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.1,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 24,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.6,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 21.4,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 1.1,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 20.4,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 3.0,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 18.9,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 10,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 15.2,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 40,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 31.9,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 0.1,
                "WME": 0,
                "ATM": 101.325,
                "SET": 20.7,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 1,
                "WME": 0,
                "ATM": 101.325,
                "SET": 27.2,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 2,
                "WME": 0,
                "ATM": 101.325,
                "SET": 32.6,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 1,
                "CLO": 4,
                "WME": 0,
                "ATM": 101.325,
                "SET": 38,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 0.8,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 23.3,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 2,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 29.8,
            }
        )
        self.tableG1.append(
            {
                "TA": 25,
                "TR": 25,
                "VEL": 0.15,
                "RH": 50,
                "MET": 4,
                "CLO": 0.5,
                "WME": 0,
                "ATM": 101.325,
                "SET": 35.9,
            }
        )

        # Test Table
        for lines in self.tableG1:
            self.result = pySET.SET(
                lines["TA"],
                lines["TR"],
                lines["VEL"],
                lines["RH"],
                lines["MET"],
                lines["CLO"],
                lines["WME"],
                lines["ATM"],
            ).getSET()
            self.assertEqual(
                float("{0:.1f}".format(self.result)), lines["SET"], "Problem"
            )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testPMVPPD']
    unittest.main()
