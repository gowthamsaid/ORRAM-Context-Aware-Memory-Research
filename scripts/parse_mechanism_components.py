#!/usr/bin/env python3
"""Quantify routed STA incremental delay by circuit region, with conservation check.

Read OpenSTA detailed path rows and classify each incremental delay, including
net delay at receiver pins. NOT transistor-level decomposition.
"""
import re,json,csv,sys,statistics
from pathlib import Path
root=Path(sys.argv[1])
rec=[]
pattern=re.compile(r'^\s*(?:(?:\d+)\s+[\d.]+\s+)?[\d.]+\s+([\d.]+)\s+([\d.]+)\s+[\^v]\s+(\S+)\s+\((\w+)\)\s*$')
for size in ('32x8','32x16'):
 for context in ('balanced','late_low'):
  for arch in ('row','word'):
   for bit in range(5):
    file=root/size/arch/context/'s11'/f'launch_{bit}.rpt'
    txt=file.read_text()
    sums={k:0.0 for k in ('launch_ff','xor_address_logic','ram_decoder','ram_selection_buffer','ram_storage_output','capture_net')}
    matched=[]
    for line in txt.splitlines():
     m=pattern.match(line)
     if not m:continue
     delay,time,name,cell=m.groups();delay=float(delay)
     if name.startswith('u_addrff_'):category='launch_ff'
     elif name.startswith('u_mix_'):category='xor_address_logic'
     elif name.startswith('u_ram/decoder_'):category='ram_decoder'
     elif name.startswith('u_ram/sel_buf_'):category='ram_selection_buffer'
     elif name.startswith('u_ram/storage_'):category='ram_storage_output'
     elif name.startswith('u_capture_'):category='capture_net'
     else:raise RuntimeError(f'Unclassified timing pin: {file}: {name}')
     sums[category]+=delay
     matched.append((name,delay))
    ma=re.search(r'(?m)^\s*([\d.]+)\s+data arrival time',txt)
    if not ma:raise RuntimeError(str(file))
    arrival=float(ma.group(1))
    if abs(sum(sums.values())-arrival)>0.00001:
     raise RuntimeError(f'Delay does not sum to path arrival: {file}: {sums}, {arrival}, rows {matched}')
    rec.append(dict(size=size,context=context,arch=arch,bit=bit,arrival_ns=arrival,**sums))
with (root/'component_delay.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rec[0]));w.writeheader();w.writerows(rec)
cases=[]
for size in ('32x8','32x16'):
 for context in ('balanced','late_low'):
  group=[r for r in rec if r['size']==size and r['context']==context]
  worst={arch:max((r for r in group if r['arch']==arch),key=lambda z:z['arrival_ns']) for arch in ('row','word')}
  keys=('launch_ff','xor_address_logic','ram_decoder','ram_selection_buffer','ram_storage_output','capture_net')
  cases.append(dict(size=size,context=context,
    row_critical_bit=worst['row']['bit'],word_critical_bit=worst['word']['bit'],
    row_minus_word_critical_path_ps=round(1000*(worst['row']['arrival_ns']-worst['word']['arrival_ns']),3),
    row_critical_component_ps={k:round(worst['row'][k]*1000,3) for k in keys},
    word_critical_component_ps={k:round(worst['word'][k]*1000,3) for k in keys}))
(root/'component_summary.json').write_text(json.dumps(dict(n_paths=len(rec),cases=cases,
 caveat='Components are *observed selected critical paths* and may differ in launch bit, endpoint, row/word selection, cell sizing, and physical topology. Incremental net delays at receiver pins are assigned to their receiver region. No intrinsic memory input-arc causal attribution without additional matched pin intervention.'),indent=2)+'\n')
print(json.dumps(cases,indent=2))
