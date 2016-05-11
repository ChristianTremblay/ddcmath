#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.

# References : https://www.deming.org/
# http://www.contesolutions.com/Western_Electric_SQC_Handbook.pdf
# http://www.fr-deming.org/WECSQ.pdf

import pandas as pd
import numpy as np
from math import fabs

from .pattern_analysis import UnnaturalPatternMixin
from .charts import IndividualChart, DistributionChart, Dashboard

class Analysis(Dashboard):
    def __init__(self, records):
        if not isinstance(records, pd.Series):
            raise TypeError('Provide data as a Pandas Series')
        self._records = records.dropna()
        self._r_chart = None
        self._xb_chart = None
        self._individual_chart = MovingRange(self._records).build_chart()
        self._distribution_chart = DistributionChart.build_chart(self._records)
        self.dashboard = Dashboard.build_dashboard(self._individual_chart,self._distribution_chart)
    
#    @property
#    def dashboard(self):
#        return self.dashboard

class ControlChart(UnnaturalPatternMixin):
    def __init__(self, records):
        if not isinstance(records, pd.Series):
            raise TypeError('Provide data as a Pandas Series')
        self._records = records.dropna()
        self._sigma = {'1':0, '2':0, '3':0}
        self._df = None
        
        if len(self._records) < 10:
            raise NotEnoughValues('Need more than 20, but not less than 10 values')
        
        self._process()
        
        
        
    def _process(self):
        raise NotImplementedError('Must be overridden')

    def _result(self):
        raise NotImplementedError('Must be overridden')
        
    @property
    def result(self):
        return self._df
    
    def _add_sigma(self, mean, UCL, LCL, df):
        sigma = ((UCL - mean)/3)
        self._sigma['1'] = sigma + mean
        self._sigma['2'] = (2 * sigma) + mean
        self._sigma['3'] = (3 * sigma) + mean
        sigma = ((mean - LCL)/3)
        self._sigma['-1'] = mean - sigma
        self._sigma['-2'] = mean - (2 * sigma)
        self._sigma['-3'] = mean - (3 * sigma)
        df = df
        df['sigma1'] = self._sigma['1']
        df['sigma2'] = self._sigma['2']
        df['sigma3'] = self._sigma['3']
        df['sigma-1'] = self._sigma['-1']
        df['sigma-2'] = self._sigma['-2']
        df['sigma-3'] = self._sigma['-3']     
        return df

    def __repr__(self):
        raise NotImplementedError('Must be overridden')

class XandR(ControlChart):
    FACTORS = { '2' : {'A2' : 1.88, 'D3' : 0, 'D4' : 3.27},
                '3' : {'A2' : 1.02, 'D3' : 0, 'D4' : 2.57},
                '4' : {'A2' : 0.73, 'D3' : 0, 'D4' : 2.28},
                '5' : {'A2' : 0.58, 'D3' : 0, 'D4' : 2.11},
                '6' : {'A2' : 0.48, 'D3' : 0, 'D4' : 2.00},
                '7' : {'A2' : 0.42, 'D3' : 0.08, 'D4' : 1.92},
                '8' : {'A2' : 0.37, 'D3' : 0.14, 'D4' : 1.86},
                '9' : {'A2' : 0.34, 'D3' : 0.18, 'D4' : 1.82},
                '10' : {'A2' : 0.31, 'D3' : 0.22, 'D4' : 1.78}
            }
    def __init__(self, records, n = None):
        if not isinstance(records, pd.Series):
            raise TypeError('Provide data as a Pandas Series')
        # Decide sample size
        self.X = {'mean' : 0, 'UCL' : 0, 'LCL' : 0}
        self.R = {'mean' : 0, 'UCL' : 0, 'LCL' : 0}
        self._size = records.count()
        
        if not n:
            for i in reversed(range(2,11)):
                if self._size / 20 > i:
                    self._n = i
                    break
                self._n = 2
        self._n_key = str(self._n)
        super(XandR,self).__init__(records)

    
    def _process(self):
        self._Xbar = []
        self._Rs = []
        for i in range(0,int(self._size/self._n)):
            serie_of_n = self._records[(int(i*self._n)):int(i*self._n)+self._n]
            self._Xbar.append(serie_of_n.mean())
            self._Rs.append(serie_of_n.max() - serie_of_n.min())
        #self.R.mean = pd.Series(self._Rs).mean()
        
        self._df_R = pd.DataFrame({'values' : self._Rs})
        self._df_R['mean'] = self._df_R['values'].mean()
        self._df_R['upper limit'] = self._df_R['mean'] * self.FACTORS[self._n_key]['D4']
        self._df_R['lower limit'] = self._df_R['mean'] * self.FACTORS[self._n_key]['D3']
        self._df_R = self._add_sigma(self._df_R['mean'][0],self._df_R['upper limit'][0], self._df_R['upper limit'][0],self._df_R)

        self._df_X = pd.DataFrame({'values' : self._Xbar})        
        self._df_X['mean'] = self._df_X['values'].mean()
        width = self._df_X['mean'] * self.FACTORS[self._n_key]['A2']
        self._df_X['upper limit'] = self._df_X['mean'] + width
        self._df_X['lower limit'] = self._df_X['mean'] - width
        self._df_X = self._add_sigma(self._df_X['mean'][0],self._df_X['upper limit'][0], self._df_X['upper limit'][0],self._df_X)

        self._df = {'R':self._df_R,
                    'Xb' : self._df_X}
        #self.unnatural_pattern_detection()
    def __repr__(self):
        return ('Not done yet')


class MovingRange(ControlChart, IndividualChart):
    
    def __init__(self, records):
        self._listmR = []
        super(MovingRange, self).__init__(records)

    def _process(self):        
        lastRec = self._records[0]
        for each in self._records[1:]:
            self._listmR.append(fabs(each - lastRec))
            lastRec = each
        self.mR = pd.Series(self._listmR)
        
        # Mean of all values from records
        self.Xb = self._records.mean()
        self.mean = self.Xb
        #print(self._listmR)
        # Mean of moving range
        self.mRb = self.mR.mean()
        if len(self._listmR) != (len(self._records) - 1):
            raise ValueError('Error processing moving range : %s, %s' % (len(self._listmR), len(self.mR)))
        
        self.UCL = self.Xb + (2.66*self.mRb)
        self.LCL = self.Xb - (2.66*self.mRb)
        
        
        df = pd.DataFrame()
        df['values'] = self._records
        #serUCL = pd.Series([self.UCL]*len(self._records), index=df.index)
        #serLCL = pd.Series([self.LCL]*len(self._records), index=df.index)
        df['mean'] = self.Xb       
        df['upper limit'] = self.UCL
        df['lower limit'] = self.LCL
        df = self._add_sigma(self.mean, self.UCL, self.LCL, df)
        df['x'] = False
        df['stratification'] = False
        df['mixture'] = False
        self._df = df

        self.unnatural_pattern_detection()
        
    def __repr__(self):
        return ('Mean : %s \nUpper limit : %s\Lower limit : %s ' % (self.mean, self.UCL, self.LCL))

        
class NotEnoughValues(Exception):
    pass