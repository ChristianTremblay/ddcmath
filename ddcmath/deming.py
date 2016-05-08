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
from bokeh.plotting import figure
from bokeh.models.sources import ColumnDataSource

def ext_range(records, n):
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

class moving_range(object):
    
    def __init__(self, records):
        self._records = records.dropna()
        self._sigma = {'1':0, '2':0, '3':0}
        if len(self._records) < 10:
            raise NotEnoughValues('Need more than 20, but not less than 10 values')
        
        self._listmR = []
        # Calculating moving range mR
        # difference between 1st and 2nd, 2nd and 3rd, ...
        # taking ansolute result
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
        
    def _last_val_was_on_other_side_of_mean(self, last, actual):
        if last * actual >= 0:
            return False
        else:
            return True         

    def unnatural_pattern_detection(self):
        for i, value in enumerate(self._df['values']):
            #print('Value : %s' % i)
            if i == 0:
                continue
            if fabs(value) > self._sigma['3']:
                print('record %s : Above zone C' % i)
                self._df.loc[self._df.index[i-1],'x'] = True
                continue
            
            if i > 2:
                if self._df['values'][i-3:i][self._df['values'] > self._sigma['2']].count() >= 2 \
                or self._df['values'][i-3:i][self._df['values'] < self._sigma['-2']].count() >= 2:
                    print('record %s : 2 out of 3 in zone A' % i)
                    print(self._df['values'][i-3:i][self._df['values'] > self._sigma['2']])
                    print(self._df['values'][i-3:i][self._df['values'] < self._sigma['-2']])                    
                    j = i                    
                    while (self._df['values'][j] > self._sigma['2']) \
                    or (self._df['values'][j] < self._sigma['-2']):
                        j -= 1
                    self._df.loc[self._df.index[j],'x'] = True
                    continue
                    
            if i > 4:
                if self._df['values'][i-5:i][self._df['values'] > self._sigma['1']].count() >= 4 \
                or self._df['values'][i-5:i][self._df['values'] < self._sigma['-1']].count() >= 4:
                    print('record %s : 4 out of 5 in zone B' % i)
                    self._df.loc[self._df.index[i-1],'x'] = True
                    continue
                
            if i > 7:
                if self._df['values'][i-8:i][self._df['values'] > self.Xb].count() >= 8 \
                or self._df['values'][i-8:i][self._df['values'] < self.Xb].count() >= 8:
                    print('record %s : 8 consecutive above / below mean' % i)
                    self._df.loc[self._df.index[i-1],'x'] = True
                    continue

    def _result(self):
        df = pd.DataFrame()
        df['values'] = self._records
        serUCL = pd.Series([self.UCL]*len(self._records), index=df.index)
        serLCL = pd.Series([self.LCL]*len(self._records), index=df.index)
        df['mean'] = self.Xb       
        df['upper limit'] = serUCL
        df['lower limit'] = serLCL
        df['sigma1'] = self._sigma['1']
        df['sigma2'] = self._sigma['2']
        df['sigma3'] = self._sigma['3']
        df['sigma-1'] = self._sigma['-1']
        df['sigma-2'] = self._sigma['-2']
        df['sigma-3'] = self._sigma['-3']
        df['x'] = False
        self._df = df
        
    @property
    def result(self):
        return self._df
        
    def control_chart(self):
        p = figure(plot_width=600, plot_height=500, x_axis_type="datetime", title='Control Chart')
        
        # add a line renderer
        src = ColumnDataSource(
            data=dict(
            x = self.result.index,
            val = self.result['values'],
            up = self.result['upper limit'],
            low = self.result['lower limit'],
            mean = self.result['mean'],
            sigma1 = self.result['sigma1'],
            sigma2 = self.result['sigma2'],
            minus_sigma1 = self.result['sigma-1'],
            minus_sigma2 = self.result['sigma-2']
            ))
        x_src = ColumnDataSource(
            data=dict(
            x = self.result[self.result['x'] == True].index,
            y = self.result['values'][self.result['x'] == True]
            ))
        p.line('x', 'val', source = src, line_width=2, line_color='blue')
        p.line('x', 'up', source = src, line_width=2, line_color='red')
        p.line('x', 'low', source = src, line_width=2, line_color='red')
        p.line('x', 'mean', source = src, line_width=2)
        # x
        p.x('x', 'y', source = x_src, size=20, color="black")
        p.line('x', 'sigma1', source = src, line_dash=[4, 4], line_color="orange", line_width=2, alpha=0.5)
        p.line('x', 'sigma2', source = src, line_dash=[4, 4], line_color="green", line_width=2, alpha=0.5)
        p.line('x', 'minus_sigma1', source = src, line_dash=[4, 4], line_color="orange", line_width=2, alpha=0.5)
        p.line('x', 'minus_sigma2', source = src, line_dash=[4, 4], line_color="green", line_width=2, alpha=0.5)
        
        #show(p) 
        return p
        
    def __repr__(self):
        return ('Xb : %s \nmRb : %s\nUpper limit : %s\Lower limit : %s ' % (self.Xb, self.mRb, self.UCL, self.LCL))

class NotEnoughValues(Exception):
    pass