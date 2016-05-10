class UnnaturalPatternMixin():
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
                    elif self._df['values'][i-1] > self._sigma['1'] \
                    or self._df['values'][i-1] < self._sigma['-1']:
                        self._df.loc[self._df.index[i-2],'x'] = True
                    else:
                        self._df.loc[self._df.index[i-3],'x'] = True

            if i >= 7:
                if self._df['values'][i-8:i][self._df['values'] > self.Xb].count() == 8 \
                or self._df['values'][i-8:i][self._df['values'] < self.Xb].count() == 8:
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
