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
from bokeh.models import HoverTool, BoxAnnotation

from collections import OrderedDict

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
            if value > self._sigma['3'] or value < self._sigma['-3']:
                self._df.loc[self._df.index[i],'x'] = True
            
            if i >= 2:
                if self._df['values'][i-3:i][self._df['values'] > self._sigma['2']].count() >= 2 \
                or self._df['values'][i-3:i][self._df['values'] < self._sigma['-2']].count() >= 2:
                    if self._df['values'][i] > self._sigma['2'] \
                    or self._df['values'][i] < self._sigma['-2']:
                        self._df.loc[self._df.index[i-1],'x'] = True
                    else:
                        self._df.loc[self._df.index[i-3],'x'] = True
                    
            if i >= 4:
                if self._df['values'][i-5:i][self._df['values'] > self._sigma['1']].count() >= 4 \
                or self._df['values'][i-5:i][self._df['values'] < self._sigma['-1']].count() >= 4:
                    if self._df['values'][i] > self._sigma['1'] \
                    or self._df['values'][i] < self._sigma['-1']:
                        self._df.loc[self._df.index[i-1],'x'] = True
                    else:
                        self._df.loc[self._df.index[i-2],'x'] = True

            if i >= 7:
                if self._df['values'][i-8:i][self._df['values'] > self.Xb].count() == 8 \
                or self._df['values'][i-8:i][self._df['values'] < self.Xb].count() >= 8:
                    print('record %s : 8 consecutive above / below mean' % i)
                    self._df.loc[self._df.index[i],'x'] = True

            # Mixture
            if i >= 8:
                if self._df['values'][i-8:i][(self._df['values'] < self._sigma['1']) & (self._df['values'] > self._sigma['-1'])].count() == 0 \
                and self._df['values'][i-8:i][self._df['values'] > self._sigma['1']].count() >= 3 \
                and self._df['values'][i-8:i][self._df['values'] < self._sigma['-1']].count() >= 3 :
                    self._df.loc[self._df.index[i],'mixture'] = True
                    
            # Stratification
            if i >= 15:
                if self._df['values'][i-15:i][(self._df['values'] < self._sigma['1']) & (self._df['values'] > self._sigma['-1'])].count() == 15 :
                    self._df.loc[self._df.index[i],'stratification'] = True

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
        df['stratification'] = False
        df['mixture'] = False
        self._df = df
        
    @property
    def result(self):
        return self._df
        
    def control_chart(self):
        #TOOLS = "hover,resize,save,pan,box_zoom,wheel_zoom,reset"
        hover = HoverTool(names=["x", "values"])
        p = figure(plot_width=600, plot_height=500, x_axis_type="datetime", title='Control Chart', tools = [hover,])
        df = self.result.reset_index()
        # add a line renderer
        src = ColumnDataSource(
            data=dict(
            x = df['index'],
            val = df['values'],
            up = df['upper limit'],
            low = df['lower limit'],
            mean = df['mean'],
            sigma1 = df['sigma1'],
            sigma2 = df['sigma2'],
            minus_sigma1 = df['sigma-1'],
            minus_sigma2 = df['sigma-2'],
            time = df['index'].apply(str)
            ))
        x_src = ColumnDataSource(
            data=dict(
            x = df['index'][df['x'] == True],
            val = df['values'][df['x'] == True],
            time = df['index'].apply(str)
            ))

        strat_src = ColumnDataSource(
            data=dict(
            x = df['index'][df['x'] == True],
            val = df['values'][df['stratification'] == True],
            time = df['index'].apply(str)
            ))        

        mix_src = ColumnDataSource(
            data=dict(
            x = df['index'][df['x'] == True],
            val = df['values'][df['mixture'] == True],
            time = df['index'].apply(str)
            ))
            
        hover = p.select(dict(type=HoverTool))
        hover.tooltips = OrderedDict([
            ('timestamp', '@time'),
            ('value', '@val'),
        ]) 
        
        zone_c_1 = BoxAnnotation(plot=p, bottom=self._df['sigma2'][0], top=self._df['sigma3'][0], fill_alpha=0.1, fill_color='orange')
        zone_b_1 = BoxAnnotation(plot=p, bottom=self._df['sigma1'][0], top=self._df['sigma2'][0], fill_alpha=0.1, fill_color='yellow')        
        zone_a_1 = BoxAnnotation(plot=p, bottom=self._df['mean'][0], top=self._df['sigma1'][0], fill_alpha=0.1, fill_color='green')        
        zone_a_2 = BoxAnnotation(plot=p, bottom=self._df['sigma-1'][0], top=self._df['mean'][0], fill_alpha=0.1, fill_color='green')        
        zone_b_2 = BoxAnnotation(plot=p, bottom=self._df['sigma-2'][0], top=self._df['sigma-1'][0], fill_alpha=0.1, fill_color='yellow')        
        zone_c_2 = BoxAnnotation(plot=p, bottom=self._df['sigma-3'][0], top=self._df['sigma-2'][0], fill_alpha=0.1, fill_color='orange')
        
        p.renderers.extend([zone_c_1, zone_b_1, zone_a_1, zone_a_2, zone_b_2, zone_c_2])
        
        p.x('x', 'val', source = x_src, name = "x", size=25, line_width=5, color="red")
        p.triangle('x', 'val', source = strat_src, size = 25, line_width=5, color="black")        
        p.triangle('x', 'val', source = mix_src, size = 25, line_width=5, color="black")        
                
        p.line('x', 'val', source = src, name = "values", line_width=2, line_color='blue')
        p.circle('x', 'val', source = src, size=10, color='blue')
        p.line('x', 'up', source = src, line_width=2, line_color='red')
        p.line('x', 'low', source = src, line_width=2, line_color='red')
        p.line('x', 'mean', source = src, line_width=2)
        # x
        p.line('x', 'sigma1', source = src, line_dash=[4, 4], line_color="green", line_width=2, alpha=0.5)
        p.line('x', 'sigma2', source = src, line_dash=[4, 4], line_color="orange", line_width=2, alpha=0.5)
        p.line('x', 'minus_sigma1', source = src, line_dash=[4, 4], line_color="green", line_width=2, alpha=0.5)
        p.line('x', 'minus_sigma2', source = src, line_dash=[4, 4], line_color="orange", line_width=2, alpha=0.5)
        
        #show(p) 
        return p
        
    def __repr__(self):
        return ('Xb : %s \nmRb : %s\nUpper limit : %s\Lower limit : %s ' % (self.Xb, self.mRb, self.UCL, self.LCL))

class NotEnoughValues(Exception):
    pass