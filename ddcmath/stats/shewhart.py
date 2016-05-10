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
from .charts import IndividualChart

class ControlChart(UnnaturalPatternMixin):
    def __init__(self, records):
        if not isinstance(records, pd.Series):
            raise TypeError('Should pass a Pandas Series')
        self._records = records.dropna()
        self._sigma = {'1':0, '2':0, '3':0}
        self._df = None
        
        if len(self._records) < 10:
            raise NotEnoughValues('Need more than 20, but not less than 10 values')
        
        self._process()

    def _process(self):
        raise NotImplementedError('Must be overridden')

    def _result(self):
        df = pd.DataFrame()
        df['values'] = self._records
        #serUCL = pd.Series([self.UCL]*len(self._records), index=df.index)
        #serLCL = pd.Series([self.LCL]*len(self._records), index=df.index)
        df['mean'] = self.Xb       
        df['upper limit'] = self.UCL
        df['lower limit'] = self.LCL
        df['sigma1'] = self._sigma['1']
        df['sigma2'] = self._sigma['2']
        df['sigma3'] = self._sigma['3']
        df['sigma-1'] = self._sigma['-1']
        df['sigma-2'] = self._sigma['-2']
        df['sigma-3'] = self._sigma['-3']
        df['x'] = False
        df['stratification'] = False
        df['mixture'] = False
        self._df = df  
                
    @property
    def result(self):
        return self._df
        
    def __repr__(self):
        return ('Xb : %s \nUpper limit : %s\Lower limit : %s ' % (self.Xb, self.UCL, self.LCL))


class XandR(ControlChart):
    
    def _process(records, n):
        facteurs = {2 : {'A2':1.88, 'D3' : 0.00, 'D4':3.27},
                     4 : {'A2':0.73, 'D3' : 0.00, 'D4':2.28}
                     }
        n = facteurs[4]
        A2 = n['A2']
        D3 = n['D3']
        D4 = n['D4']
        
        df = pd.DataFrame()
        df['Avg'] = records.resample('h')
        df['Min'] = records.resample('h',how=np.min)
        df['Max'] = records.resample('h',how=np.max)
        df['Range'] = (records.resample('h',how=np.max) - records.resample('h',how=np.min))
        
        Xb = df['Avg'].mean()
        Rb = df['Range'].mean()
        R_UCL = Rb * D4
        R_LCL = Rb * D3
    
        
        Xb_UCL = Xb + ((Rb * A2))
        Xb_LCL = Xb - ((Rb * A2))
        
        df_R = pd.DataFrame()
        df_R['R'] = df['Range']
        df_R['UCL'] = pd.Series([R_UCL]*len(df_R['R']), index=df.index)
        df_R['LCL'] = pd.Series([R_LCL]*len(df_R['R']), index=df.index)
        df_R.plot()
        
        df_Xb = pd.DataFrame()
        df_Xb['Avg'] = df['Avg']
        df_Xb['UCL'] = pd.Series([Xb_UCL]*len(df_Xb['Avg']), index=df.index)
        df_Xb['LCL'] = pd.Series([Xb_LCL]*len(df_Xb['Avg']), index=df.index)
        df_Xb.plot()
        return df_Xb

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
        #print(self._listmR)
        # Mean of moving range
        self.mRb = self.mR.mean()
        if len(self._listmR) != (len(self._records) - 1):
            raise ValueError('Error processing moving range : %s, %s' % (len(self._listmR), len(self.mR)))
        
        self.UCL = self.Xb + (2.66*self.mRb)
        self.LCL = self.Xb - (2.66*self.mRb)
        sigma = ((self.UCL - self.Xb)/3)
        self._sigma['1'] = sigma + self.Xb
        self._sigma['2'] = (2 * sigma) + self.Xb
        self._sigma['3'] = (3 * sigma) + self.Xb
        self._sigma['-1'] = self.Xb - sigma
        self._sigma['-2'] = self.Xb - (2 * sigma)
        self._sigma['-3'] = self.Xb - (3 * sigma)
        self._result()
        self.unnatural_pattern_detection()
        
#    def _last_val_was_on_other_side_of_mean(self, last, actual):
#        if last * actual >= 0:
#            return False
#        else:
#            return True         

class NotEnoughValues(Exception):
    pass