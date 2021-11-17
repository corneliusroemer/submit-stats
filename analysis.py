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
df['days_diff'] = ( df.date_submitted-df.date).dt.days
df['days_diff'].describe()
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
 'University Hospitals of Geneva, Laboratory of Virology': 'HUG, Laboratory of Virology and the Health2030 Genome Center',
 'Center for Emerging Viral Diseases, Geneva University Hospitals and University of Geneva and Department of Microbiology and Molecular Medicine, Faculty of Medicine, University of Geneva.':'HUG, Laboratory of Virology and the Health2030 Genome Center',
 'Dr Risch Laboratory': 'Risch',
 'Microbiology_DrRisch_Buchs': 'Risch',
 'Microbiology, Dr. Risch': 'Risch',
 'Microbiology Lab Dr. Risch Buchs': 'Risch',
 }

def normalize(lab):
    if(lab in lab_normalisation):
        return lab_normalisation[lab]
    else:
        return lab
#%%
df['lab']=df.submitting_lab.apply(normalize)
# %%
df['lab'].value_counts()
#%%
def quantile_q(q):
    def quantile(x):
        return round(np.percentile(x, q))
    quantile.__name__ = 'q' + str(q)
    return quantile
#%%
df_pivot = df.pivot_table(index= ['lab','week'],values=['days_diff'],aggfunc=['count','min',quantile_q(5),quantile_q(25),quantile_q(50),quantile_q(75),quantile_q(95),'max'])
df_pivot.to_csv('days_diff_by_submitting_lab_and_week.tsv',sep='\t')
df_pivot
# %%
df_pivot.xs('2021-35', level=1, drop_level=False).sort_values(by=[('count','days_diff')],ascending=False)
df_pivot.xs('2021-34', level=1, drop_level=False).sort_values(by=[('count','days_diff')],ascending=False)
# %%
