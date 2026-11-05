#!/usr/bin/env python3
"""Summarize actual OpenSTA data; report NULL effects rather than making up gains."""
import csv,json,pathlib,re,sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
contexts=['reference','late_addr_lowbits','late_addr_highbits','heavy_outputs','tight_output']
rows=[]
for context in contexts:
 for arch in ('row','word'):
  file=root/arch/context/'read_path.rpt'
  txt=file.read_text()
  if 'Startpoint:' not in txt:raise SystemExit(f'BLOCKED: no timing path {file}')
  sec='Startpoint:'+txt.split('Startpoint:',1)[1].split('Startpoint:',1)[0]
  def read(pattern,key):
   m=re.search(pattern,sec,re.M)
   if not m:raise SystemExit(f'BLOCKED: missing {key} in {file}')
   return m.group(1).strip()
  rows.append({'context':context,'architecture':arch,
   'slack_ns':float(read(r'^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)','slack')),
   'arrival_ns':float(read(r'^\s*([+-]?\d+\.\d+)\s+data arrival time','arrival')),
   'startpoint':read(r'^Startpoint:\s*(.+)$','startpoint').split(' (')[0],
   'endpoint':read(r'^Endpoint:\s*(.+)$','endpoint').split(' (')[0]})
with (out/'results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
by={(r['context'],r['architecture']):r for r in rows}
def winner(c):
 d=by[(c,'row')]['slack_ns']-by[(c,'word')]['slack_ns']
 return ('row' if d>.020 else 'word' if d<-.020 else 'tie'),d
base=winner('reference')[0]
flips=[{'context':c,'winning_architecture':winner(c)[0],'difference_ns':winner(c)[1]}
 for c in contexts[1:] if winner(c)[0] not in ('tie',base) and base!='tie']
status='GO_TO_TOP_LEVEL_INTEGRATION' if flips else 'NO_REVERSAL_IN_ISOLATED_BOUNDARY_SCREEN'
decision={'status':status,'reference_winner':base,'reversals':flips,
 'limitations':['Fixed physical checkpoints, estimated placement RC, no top-level integration',
 'Exogenously varying input budgets can trivially change slack with no physical delay changes',
 'Outcome does not establish publication novelty or benefit of an optimization algorithm']}
(out/'decision.json').write_text(json.dumps(decision,indent=2)+'\n')
lines=['# ORRAM context-aware feasibility: measured results','',f'**Decision: {status}**','','|Scenario|Row slack (ns)|Word slack (ns)|Winner (>20 ps)|','|---|---:|---:|---|']
for c in contexts:
 w,d=winner(c);lines.append(f"|{c}|{by[(c,'row')]['slack_ns']:.5f}|{by[(c,'word')]['slack_ns']:.5f}|{w}|")
lines+=['','**Interpretation:** a preference reversal in this fixed-block boundary screen is *necessary evidence* only.',
 'Real enclosing circuits, matched full-route extracted parasitics, held-out designs and proper baselines are required before a strong research GO.',
 'If no reversal occurs, treat as a null result for these configurations, not a refutation of all context-aware methods.']
(out/'REPORT.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))