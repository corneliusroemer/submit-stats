#%%
import pandas as pd
import math
import datetime as dt   
import matplotlib.pyplot as plt
import numpy as np
#%%
# df = pd.read_csv('meta_swiss_narrow.tsv', sep='\t',parse_dates=['date','date_submitted'])
df = pd.read_csv('meta_switzerland.tsv', sep='\t',parse_dates=['date','date_submitted'])

# %%
df['week'] = df.date_submitted.apply(lambda x: f"{x.year}-{x.week:02}")
df.clock_deviation = pd.to_numeric(df.clock_deviation,errors='coerce')
#%%
# Normalize all the labs

#%%
# plot = df.clock_deviation.hist(bins=20)
# plot.set_xlim(-50,30)
#%%
# axes = df['date'].hist(bins=20)
# axes.set_xlim(dt.date(2021,8,1),dt.date(2021,9,1))
# fig = plt.gcf()
# fig.autofmt_xdate()
# ax = plt.gca()
# ax.set_ylabel('Submitted sequences')
# ax.set_xlabel('Submission date')
# ax.set_title('Turkish sequences by submission date')
# #%%
# df.sort_values(by='date').tail()
# %%
# df = df[df.date < dt.datetime(2021,5,1)]
# df = df[df.date > dt.datetime(2021,4,1)]
## Calculate median time difference between date and date_submitted, grouped by submitting_lab
df['days_diff'] = ( df.date_submitted-df.date).dt.days
df['days_diff'].describe()
#%%
# n = math.ceil((df.days_diff.max() - df.days_diff.min()))
# plot = df['days_diff'].hist(bins = n)
# plot.set_xlim(0,50)
# fig = plt.gcf()
# ax = plt.gca()
# ax.set_ylabel('# of sequences')
# ax.set_xlabel('Days passed between sampling and submission')
# ax.set_title('Swiss sequences (sampled in July) by sequencing turnaround')

# #%%
# df.groupby(['submitting_lab']).days_diff.median()
# #%%
# Calculate median time difference between date and date_submitted, grouped by submitting_lab
df['days_diff'] = (df.date_submitted -df.date).dt.days
df['days_diff'].describe()
#%%
# # df.groupby(['submitting_lab']).days_diff.median()
# df.groupby(['submitting_lab']).days_diff.mean()
# # df.groupby(['submitting_lab']).days_diff.count()
# print(0.1)
# df.groupby(['submitting_lab']).days_diff.quantile(q=0.1)
# print(0.25)
# df.groupby(['submitting_lab']).days_diff.quantile(q=0.25)
# print(0.5)
# df.groupby(['submitting_lab']).days_diff.quantile(q=0.5)
# print(0.75)
# df.groupby(['submitting_lab']).days_diff.quantile(q=0.75)
# print(0.9)
# df.groupby(['submitting_lab']).days_diff.quantile(q=0.9)
#%%
def quantile_q(q):
    def quantile(x):
        return round(np.percentile(x, q))
    quantile.__name__ = 'q' + str(q)
    return quantile
#%%
df_pivot = df.pivot_table(index= ['lab','week'],values=['days_diff'],aggfunc=['count','min',quantile_q(5),quantile_q(25),quantile_q(50),quantile_q(75),quantile_q(95),'max'])
# df_pivot = df_pivot.reindex(df_pivot['median'].sort_values(by='days_diff',ascending=True).index)
df_pivot.to_csv('days_diff_by_submitting_lab_and_week.tsv',sep='\t')
df_pivot
#%%
#%%
# df.columns
# %%
# for c in [ 'date', 'region', 'country', 'division', 'location', 'region_exposure', 'country_exposure', 'division_exposure', 'segment',  'host', 'age', 'sex', 'Nextstrain_clade', 'pango_lineage', 'GISAID_clade', 'originating_lab', 'submitting_lab', 'authors',  'date_submitted', 'sampling_strategy',  'divergence', 'nonACGTN', 'rare_mutations', 'snp_clusters', 'QC_missing_data', 'QC_mixed_sites', 'QC_rare_mutations', 'QC_snp_clusters', 'clock_deviation', 'days_diff']: 
#     print(f"\n---- {c} ---")
#     print(df[c].value_counts())
# # %%
# quick = df[df.days_diff < 10]
# slow = df[df.days_diff > 30]
# # %%
# df.pivot_table(index='submitting_lab',values='authors',aggfunc='first')

# # 
# %%
# df.pivot_table(index=['submitting_lab','week'],values=['days_diff'],aggfunc='median').to_csv('delay_by_lab_week.tsv',sep='\t')
# %%

# df.submitting_lab.unique()
# %%
lab_normalisation = {'Clinical Bacteriology':'University Hospital Basel, Clinical Bacteriology',
 'Department of Biosystems Science and Engineering, ETH Zurich':'Department of Biosystems Science and Engineering, ETH Zürich',
 'Department of Biosystems Science and Engineering, ETH Zurich':'Department of Biosystems Science and Engineering, ETH Zürich',
 'University Hospitals of Geneva Laboratory of Virology': 'HUG, Laboratory of Virology and the Health2030 Genome Center',
 'Institute of Medical Virology': 'Institute of Medical Virology, University of Zurich',
 'Institute for Infectious Diseases, University of Bern, Switzerland': 'Institute for Infectious Diseases, University of Bern',
 'Institute for Infectious Diseases': 'Institute for Infectious Diseases, University of Bern',
 'Swiss National Reference Centre for Influenza Virology laboratory, CNRI': 'Swiss National Reference Centre for Influenza',
 'University Hospital Basel, Switzerland':'University Hospital Basel, Clinical Bacteriology',
 'University Hospital Basel, Clinical Virology':'University Hospital Basel, Clinical Bacteriology',
 'University Hospital Basel, Labormedizin':'University Hospital Basel, Clinical Bacteriology',
 'Laboratory of genomics and metagenomics, Institute of Microbiology, University Hospital Centre and University of Lausanne, Switzerland': 'Laboratory of genomics and metagenomics, Lausanne',
 'Laboratory of genomics and metagenomics': 'Laboratory of genomics and metagenomics, Lausanne',
 'Center for Laboratory Medicine': 'Center for Laboratory Medicine St. Gallen',
 'Hagmattstrasse 14, 4123 Allschwil, Switzerland': 'Viollier AG',
 'Switzerland': 'Department of Biosystems Science and Engineering, ETH Zürich',
 'Geneva Centre for Emerging Viral Diseases': 'HUG, Laboratory of Virology and the Health2030 Genome Center',
 'University Hospitals of Geneva, Laboratory of Virology': 'HUG, Laboratory of Virology and the Health2030 Genome Center'}

def normalize(lab):
    if(lab in lab_normalisation):
        return lab_normalisation[lab]
    else:
        return lab
    
#%%
df['lab']=df.submitting_lab.apply(normalize)
# %%
df['lab'].value_counts()


# %%
