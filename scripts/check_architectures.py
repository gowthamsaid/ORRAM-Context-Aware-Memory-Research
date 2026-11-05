#!/usr/bin/env python3
"""Gate on identical logical interfaces plus distinct implemented cell/net topology."""
import collections,hashlib,json,pathlib,re,sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
models={k:(root/k/'behavioral.v').read_bytes() for k in ('row','word')}
if models['row']!=models['word']:raise SystemExit('BLOCKED: behavioral models differ')
for k in ('row','word'):
 s=models[k].decode()
 for name in ('RAM32x8','addr_rw','we','D','Q','clk'):
  if not re.search(r'\b'+name+r'\b',s):raise SystemExit('BLOCKED: missing interface '+name)
def topology(k):
 t=(root/k/'ram.def').read_text()
 section=re.search(r'\bCOMPONENTS\s+\d+\s*;(.*?)\bEND\s+COMPONENTS',t,re.S)
 net_section=re.search(r'\bNETS\s+\d+\s*;(.*?)\bEND\s+NETS',t,re.S)
 if not section or not net_section:raise SystemExit('BLOCKED: malformed DEF')
 inst=dict(re.findall(r'(?m)^\s*-\s+(\S+)\s+(\S+)',section.group(1)))
 hist=collections.Counter(inst.values())
 connections=[]
 for entry in re.findall(r'(?ms)^\s*-\s+.*?;',net_section.group(1)):
  header=re.split(r'\s+\+\s+(?:ROUTED|FIXED|COVER|NEW|SHIELD|NOSHIELD)\b',entry,1)[0]
  pins=[]
  for cell,pin in re.findall(r'\(\s+(\S+)\s+(\S+)\s+\)',header):
   master='PORT' if cell=='PIN' else inst.get(cell,'UNKNOWN')
   pins.append((master,pin))
  if len(pins)>1:connections.append(tuple(sorted(pins)))
 if not hist or not connections:raise SystemExit('BLOCKED: no cell/net connectivity')
 sig=hashlib.sha256(json.dumps(sorted(connections)).encode()).hexdigest()
 return hist,sig,len(connections)
a,asig,ac=topology('row');b,bsig,bc=topology('word')
result={'identical_behavioral_models':True,
 'model_sha256':hashlib.sha256(models['row']).hexdigest(),
 'row_cell_histogram':dict(a),'word_cell_histogram':dict(b),
 'row_nets':ac,'word_nets':bc,'structurally_distinct':(a!=b or asig!=bsig),
 'connectivity_hashes':{'row':asig,'word':bsig}}
(out/'architecture_contract.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not result['structurally_distinct']:raise SystemExit('NO-GO: architectures collapsed to same structure')