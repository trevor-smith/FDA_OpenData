########## MORE DATA EXPLORING ############

### IMPORTS ###
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import pandas as pd
import numpy as np

### READ IN DATA ###
df = pd.read_csv('patients_aggv6.csv', header=None, names = ['safetyreportid', '@epoch', 'receivedate', 'serious','transmissiondate', 'medicinalproduct', 'drugcharacterization'])

### DATA CLEANING ###

# rename columns
# df.rename(columns={'10216050':'safetyreportid' , '1417466131.85916':'@epoch' ,'20111229':'receivedate' , 'serious':'serious' , '20141002':'transmissiondate','DIOVAN HCT CO-DIOVAN (HYDROCHLOROTHIAZIDE, VALSARTAN)':'medicinalproduct' ,'drugcharacterization':'drugcharacterization'  }, inplace=True)

# dropping bad column and parsing dates
df = df[df.medicinalproduct != 'medicinalproduct']
df['receivedate'] = df['receivedate'].astype(str)
df['receivedate'] = pd.to_datetime(df['receivedate'])

### EARLY EXPLORING ###

# we want to only look at the suspect drugs
# this will eliminate drugs like aspirin from showing up a lot
suspect = df[(df.drugcharacterization == 1)]

# now let's look at the drugs that appear the most
# humira, enbrel, mirena = top 3
grouped = suspect.groupby(['medicinalproduct']).size().order(ascending=False)[:25]
print grouped

# now let's look at the biggest one day spikes
grouped = suspect.groupby(['medicinalproduct', 'receivedate']).size().order(ascending=False)[:25]
print grouped

# let's dig further into Humira
humira = df[(df.medicinalproduct == 'HUMIRA') & (df.drugcharacterization == 1)]
humira_grouped = humira.groupby(['receivedate']).size()
print humira_grouped

# let's visualize this in a line chart
# %pylab inline
# %matplotlib inline
# humira_grouped.plot(kind='line', figsize=(15,12))

# let's now visualize the Byetta results
byetta = df  & (df.drugcharacterization == 1)]
byetta_grouped = byetta.groupby(['receivedate']).size()
byetta_grouped.plot(kind='line', figsize=(15,12), style='k', c='b', linewidth=1.0)
pd.stats.moments.rolling_mean(byetta_grouped, 30).plot(style='k-', c='r', linewidth=2.0)
plt.show()

# let's now just visualize all drugs
suspect = df[(df.drugcharacterization == 1)]
suspect_grouped = suspect.groupby(['receivedate']).size()
suspect_grouped.plot(style='k', figsize=(15,12), c='b', linewidth=1.0, label='Daily')
pd.stats.moments.rolling_mean(suspect_grouped, 60).plot(style='k-', c='r', linewidth=2.0, label='60 Day Moving Avg')
pd.stats.moments.rolling_mean(suspect_grouped, 30).plot(style='k--', c='g', linewidth=2.0, label='30 Day Moving Avg')
plt.ylabel('number of adverse events over time')
plt.xlabel('date')
plt.title('FDA: Number of Adverse Events Over Time')
plt.grid(True)
plt.legend(loc='upper center', shadow=True)
plt.show()
