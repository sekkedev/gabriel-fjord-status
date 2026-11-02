import pandas as pd, json, numpy as np
df=pd.read_csv('data/resampled_data_2015-05-12_to_2026-10-20.csv',parse_dates=['ts'])
P=['temperature','salinity','oxygen','turbidity','fluorescence']
last=df.ts.max()
def lay(x):
    return x.assign(layer=pd.cut(x.pressure_dbar,[0,2,9,20],labels=['surface','middle','deep']))
def means(x): return lay(x).groupby('layer',observed=True)[['temperature','salinity','oxygen']].mean().round(2).to_dict('index')
out={'last':str(last)}
lp=df[df.ts==last].sort_values('pressure_dbar')
out['profile']=lp[['pressure_dbar']+P].round(2).values.tolist()
# latest dive's raw samples, split at the deepest one: the CTD goes down slowly and comes up fast, so the ascent lags
raw=pd.read_csv('data/raw_2026-09-20_to_2026-10-20.csv',parse_dates=['ts'])
c=raw[(raw.ts==last)&(raw.salinity>1)].sort_values('seq')   # salinity ~0 means the sensor is still in air
assert len(c), f'no raw samples for {last}: download the raw export for that dive'
k=c.pressure_dbar.values.argmax(); c=c[['pressure_dbar']+P].round(2).values.tolist()
out['cast']={'down':c[:k+1],'up':c[k:]}
r=df[df.ts>last-pd.Timedelta(days=30)]
dep=sorted(r.pressure_dbar.unique()); print('depths',dep, r.groupby('pressure_dbar').size().to_dict())
piv={p:r.pivot_table(index='ts',columns='pressure_dbar',values=p) for p in P}
# every matrix shares one row per dive, so a parameter that is all-NaN in a dive can't shift its rows
ts=pd.DatetimeIndex(sorted(r.ts.unique()))
out['heat']={'ts':[t.strftime('%Y-%m-%dT%H:%M') for t in ts],'depths':dep,
 **{p:[[None if pd.isna(v) else round(float(v),2) for v in row] for row in piv[p].reindex(index=ts,columns=dep).values] for p in P}}
W=pd.Timedelta(days=7); M=pd.Timedelta(days=30)
out['week']={'now':means(df[df.ts>last-W]),'prev':means(df[(df.ts>last-2*W)&(df.ts<=last-W)])}
out['month']={'now':means(df[df.ts>last-M]),'prev':means(df[(df.ts>last-2*M)&(df.ts<=last-M)])}
oct=df[(df.ts.dt.month==10)&(df.ts.dt.day<=20)]
out['normal']={'years':sorted(int(y) for y in oct[oct.ts.dt.year<2026].ts.dt.year.unique()),
 'past':means(oct[oct.ts.dt.year<2026]),'now':means(oct[oct.ts.dt.year==2026])}
# how many of the 20 days each earlier year covers, so the page can say when a year is thin
po=oct[oct.ts.dt.year<2026]
out['normal']['days']={int(y):int(n) for y,n in po.groupby(po.ts.dt.year).ts.apply(lambda s:s.dt.date.nunique()).items()}
so=df[(df.ts.dt.month.isin([9,10]))&(df.pressure_dbar>=12.5)]
out['deepOxygen']={int(k):round(v,1) for k,v in so.groupby(so.ts.dt.year).oxygen.mean().items()}
# daily surface series last 30d
s=df[(df.ts>last-M)&(df.pressure_dbar==0.5)].set_index('ts').resample('D')[['temperature','salinity','oxygen','turbidity']].mean()
print(s.round(2).to_string())
deep=df[(df.ts>last-M)&(df.pressure_dbar>=14.5)].set_index('ts').resample('D').oxygen.mean(); print(deep.round(1).to_string())
json.dump(out,open("prototype/data.json","w"),separators=(',',':'))
print(json.dumps({k:out[k] for k in ['week','month','normal','deepOxygen']},indent=0))
