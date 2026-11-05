#!/usr/bin/env python3
from pathlib import Path
import csv,json,re,statistics,sys
train=Path(sys.argv[1]);test=Path(sys.argv[2]);out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
def slack(path):
 m=re.search(r'(?m)^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)',path.read_text())
 if not m:raise RuntimeError(str(path))
 return float(m.group(1))
rows=[]
for mode in ('balanced','late_low','late_high'):
 for seed in (11,23,37):
  root=test if mode=='late_high' else train
  p={a:root/a/mode/('s'+str(seed)) for a in ('row','word')}
  early={a:slack(d/'read_reg_to_reg.rpt') for a,d in p.items()}
  routed={a:slack(d/'routed_read_path.rpt') for a,d in p.items()}
  overall={a:slack(d/'routed_overall.rpt') for a,d in p.items()}
  valid=all(abs(routed[a]-overall[a])<0.001 for a in p)
  chosen=max(early,key=early.get)
  oracle=max(routed,key=routed.get)
  rows.append(dict(mode=mode,seed=seed,selected=chosen,oracle=oracle,full_path_agrees=valid,
   row_minus_word_ps=1000*(routed['row']-routed['word']),
   selected_gain_ps=1000*(routed[chosen]-routed['word']),
   oracle_regret_ps=1000*(routed[oracle]-routed[chosen])))
with (out/'pairs.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(n=len(rows),n_correct=sum(x['selected']==x['oracle'] for x in rows),
 heldout_correct=sum(x['selected']==x['oracle'] for x in rows if x['mode']=='late_high'),
 mean_gain_ps=statistics.mean(x['selected_gain_ps'] for x in rows),
 mean_regret_ps=statistics.mean(x['oracle_regret_ps'] for x in rows),
 full_path_matches=sum(x['full_path_agrees'] for x in rows),rows=rows,
 limitation='Only 32x8, three seeds, crafted contexts; requires both candidates placed.')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
assert len(rows)==9
