#!/usr/bin/env python3
"""Parse validated per-launch OpenSTA timing reports and compare architectures.

All values from the FIRST (worst) path for each launch FF, extracted using
original pinned 32x8/32x16 routed ODB + SDC + SPEF.
"""
import json,re,sys,statistics,csv
from pathlib import Path
root=Path(sys.argv[1])
rows=[]
for size in ('32x8','32x16'):
 for mode in ('balanced','late_low'):
  for arch in ('row','word'):
   for bit in range(5):
    src=root/size/arch/mode/'s11'/f'launch_{bit}.rpt'
    txt=src.read_text()
    first=txt.split('Startpoint:',1)[1].split('Startpoint:',1)[0]
    def match(pattern):
     m=re.search(pattern,first,re.M)
     if not m: raise RuntimeError(f'No match {pattern} in {src}: {first[-1300:]}')
     return m.group(1)
    rows.append(dict(size=size,context=mode,arch=arch,bit=bit,
      startpoint=match(r'^\s*(u_addrff_\d+[^\n]*)'),
      endpoint=match(r'(?m)^Endpoint:\s*(.*)'),
      arrival_ns=float(match(r'^\s*([+-]?\d+\.\d+)\s+data arrival time')),
      slack_ns=float(match(r'^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)'))))
result=[]
for size in ('32x8','32x16'):
 for mode in ('balanced','late_low'):
  subset={(r['arch'],r['bit']):r for r in rows if r['size']==size and r['context']==mode}
  diffs=[1000*(subset[('row',i)]['arrival_ns']-subset[('word',i)]['arrival_ns']) for i in range(5)]
  result.append(dict(size=size,context=mode,
    row_minus_word_arrival_ps_by_bit=[round(x,3) for x in diffs],
    max_row_arrival_ns=max(subset[('row',i)]['arrival_ns'] for i in range(5)),
    max_word_arrival_ns=max(subset[('word',i)]['arrival_ns'] for i in range(5)),
    row_critical_launch_bits=[i for i in range(5) if subset[('row',i)]['arrival_ns']==max(subset[('row',j)]['arrival_ns'] for j in range(5))],
    word_critical_launch_bits=[i for i in range(5) if subset[('word',i)]['arrival_ns']==max(subset[('word',j)]['arrival_ns'] for j in range(5))]))
with (root/'per_address.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]))
 w.writeheader();w.writerows(rows)
(root/'summary.json').write_text(json.dumps(dict(cases=result,count=len(rows),units='ns except per-address difference ps',caveat='Read-path arrivals include preceding address-generation logic; address-specific *intrinsic memory arc* is not isolated by this experiment.'),indent=2)+'\n')
print(json.dumps({'cases':result,'total_paths':len(rows)},indent=2))
