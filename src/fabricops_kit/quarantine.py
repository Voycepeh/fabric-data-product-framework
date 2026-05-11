from __future__ import annotations
import pandas as pd

def split_valid_quarantine_and_failures(df:pd.DataFrame, failure_evidence:list[dict]):
    """Split source rows into valid/quarantine and return one-row-per-failure evidence."""
    if not failure_evidence: return df.copy(), df.iloc[0:0].copy(), pd.DataFrame([])
    qidx=set()
    ev=[]
    for f in failure_evidence:
      for i,row in df.iterrows():
        c=f.get('column_name','')
        if ',' in c: continue
        if c in row and row[c]==f.get('failed_value'): qidx.add(i); ev.append({'row_index':i,**f})
    quarantine=df.loc[sorted(qidx)] if qidx else df.iloc[0:0].copy()
    valid=df.drop(index=list(qidx))
    return valid, quarantine, pd.DataFrame(ev)
