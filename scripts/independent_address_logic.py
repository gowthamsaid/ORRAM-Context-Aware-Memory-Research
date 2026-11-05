#!/usr/bin/env python3
"""Independent logic-cone stress: XOR-mixing address producer (no buffer-delay padding).
Matched RTL gates are identical for row and word architecture in each context.
Different contexts are deliberately different functions, so NOT an app PPA comparison.
"""
import sys
from pathlib import Path
if len(sys.argv)!=3 or sys.argv[1] not in ('balanced','late_low'):
 raise SystemExit('usage: independent_address_logic.py balanced|late_low DEST')
mode=sys.argv[1]
out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
s=['module integrated_top(input clk,input [4:0] addr_in,input [7:0] data_in,',
   'input write_enable,output [7:0] data_out);',
   'wire [4:0] addr_q;wire [4:0] addr_mem;wire [7:0] mem_q;']
for i in range(5):
 s.append(f'DFF_X1 u_addrff_{i} (.CK(clk),.D(addr_in[{i}]),.Q(addr_q[{i}]));')
for i in range(5):
 depth=3 if mode=='late_low' and i in (0,1) else 1
 last=f'addr_q[{i}]'
 for j in range(depth):
  nxt=f'addr_mem[{i}]' if j==depth-1 else f'logic_{i}_{j}'
  if j!=depth-1:s.append(f'wire {nxt};')
  # Genuine XOR logic with varied signal inputs, not a BUF delay chain.
  other=f'addr_q[{(i+j+1)%5}]'
  s.append(f'XOR2_X1 u_mix_{i}_{j} (.A({last}),.B({other}),.Z({nxt}));')
  last=nxt
s.append('RAM32x8 u_ram(.clk(clk),.D(data_in),.Q(mem_q),.addr_rw(addr_mem),.we(write_enable));')
for i in range(8):
 s.append(f'DFF_X1 u_capture_{i} (.CK(clk),.D(mem_q[{i}]),.Q(data_out[{i}]));')
s.append('endmodule')
out.write_text('\n'.join(s)+'\n')
print('INDEPENDENT_XOR_WRAPPER',mode,out)
