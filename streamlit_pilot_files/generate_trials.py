import pandas as pd, random
random.seed(42)
df = pd.read_excel("metadata.xlsx")
qs=['word','severity','similarity']
tr=[]
[tr.extend([{**r.to_dict(),'question':q} for q in qs]) for _,r in df.iterrows()]
random.shuffle(tr)
[p.update({'trial':i+1}) for i,p in enumerate(tr)]
pd.DataFrame(tr).to_csv('trials.csv',index=False)
print('done')
