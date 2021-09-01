#%%
import pandas as pd
import math
import datetime as dt   
import matplotlib.pyplot as plt
import numpy as np
#%%
# df = pd.read_csv('meta_swiss_narrow.tsv', sep='\t',parse_dates=['date','date_submitted'])
df = pd.read_csv('meta_switzerland.tsv', sep='\t',parse_dates=['date','date_submitted'])

#%%
df = df[df.date > dt.datetime(2021,8,1)]
#%%
df.clock_deviation = pd.to_numeric(df.clock_deviation,errors='coerce')
#%%
plot = df.clock_deviation.hist(bins=20)
plot.set_xlim(-50,30)
#%%
axes = df['date'].hist(bins=20)
axes.set_xlim(dt.date(2021,8,1),dt.date(2021,9,1))
fig = plt.gcf()
fig.autofmt_xdate()
ax = plt.gca()
ax.set_ylabel('Submitted sequences')
ax.set_xlabel('Submission date')
ax.set_title('Turkish sequences by submission date')
#%%
df.sort_values(by='date').tail()
# %%
df = df[df.date < dt.datetime(2021,8,1)]
df = df[df.date > dt.datetime(2021,7,1)]
## Calculate median time difference between date and date_submitted, grouped by submitting_lab
df['days_diff'] = ( df.date_submitted-df.date).dt.days
df['days_diff'].describe()
#%%
n = math.ceil((df.days_diff.max() - df.days_diff.min()))
plot = df['days_diff'].hist(bins = n)
plot.set_xlim(0,50)
fig = plt.gcf()
ax = plt.gca()
ax.set_ylabel('# of sequences')
ax.set_xlabel('Days passed between sampling and submission')
ax.set_title('Swiss sequences (sampled in July) by sequencing turnaround')

#%%
df.groupby(['submitting_lab']).days_diff.median()
#%%
# Calculate median time difference between date and date_submitted, grouped by submitting_lab
df['days_diff'] = (df.date - df.date_submitted).dt.days
df['days_diff'].describe()
#%%
# df.groupby(['submitting_lab']).days_diff.median()
df.groupby(['submitting_lab']).days_diff.mean()
# df.groupby(['submitting_lab']).days_diff.count()
print(0.1)
df.groupby(['submitting_lab']).days_diff.quantile(q=0.1)
print(0.25)
df.groupby(['submitting_lab']).days_diff.quantile(q=0.25)
print(0.5)
df.groupby(['submitting_lab']).days_diff.quantile(q=0.5)
print(0.75)
df.groupby(['submitting_lab']).days_diff.quantile(q=0.75)
print(0.9)
df.groupby(['submitting_lab']).days_diff.quantile(q=0.9)
#%%
def quantile_q(q):
    def quantile(x):
        return round(np.percentile(x, q))
    quantile.__name__ = 'q' + str(q)
    return quantile
#%%
df.pivot_table(index= ['submitting_lab'],values=['days_diff'],aggfunc=['count','mean','min',quantile_q(5),quantile_q(25),quantile_q(50),quantile_q(75),quantile_q(95),'max'])

#%%
df.columns
# %%
for c in [ 'date', 'region', 'country', 'division', 'location', 'region_exposure', 'country_exposure', 'division_exposure', 'segment',  'host', 'age', 'sex', 'Nextstrain_clade', 'pango_lineage', 'GISAID_clade', 'originating_lab', 'submitting_lab', 'authors',  'date_submitted', 'sampling_strategy',  'divergence', 'nonACGTN', 'rare_mutations', 'snp_clusters', 'QC_missing_data', 'QC_mixed_sites', 'QC_rare_mutations', 'QC_snp_clusters', 'clock_deviation', 'days_diff']: 
    print(f"\n---- {c} ---")
    print(df[c].value_counts())
# %%
quick = df[df.days_diff < 10]
slow = df[df.days_diff > 30]
# %%

