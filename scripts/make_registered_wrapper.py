#!/usr/bin/env python3
"""Generate functionally matched registered test wrappers. No synthesis."""
from pathlib import Path
import sys
if len(sys.argv)!=3 or sys.argv[1] not in ("balanced","late_low"):
    raise SystemExit("usage: make_registered_wrapper.py balanced|late_low FILE.v")
mode=sys.argv[1];out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
lines=["module integrated_top(input clk, input [4:0] addr_in, input [7:0] data_in,",
       "input write_enable, output [7:0] data_out);",
       "wire [4:0] addr_q; wire [4:0] addr_mem; wire [7:0] mem_q;"]
for i in range(5):
    lines.append(f"DFF_X1 u_addrff_{i} (.CK(clk), .D(addr_in[{i}]), .Q(addr_q[{i}]));")
for i in range(5):
    stages=5 if mode=="late_low" and i in (0,1) else 1
    prev=f"addr_q[{i}]"
    for s in range(stages):
        nxt=f"b_{i}_{s}" if s<stages-1 else f"addr_mem[{i}]"
        if s<stages-1: lines.append(f"wire {nxt};")
        lines.append(f"BUF_X1 u_address_buffer_{i}_{s} (.A({prev}), .Z({nxt}));")
        prev=nxt
lines.append("RAM32x8 u_ram(.clk(clk), .D(data_in), .Q(mem_q), .addr_rw(addr_mem), .we(write_enable));")
for i in range(8):
    lines.append(f"DFF_X1 u_capture_{i} (.CK(clk), .D(mem_q[{i}]), .Q(data_out[{i}]));")
lines.append("endmodule")
out.write_text("\n".join(lines)+"\n")
print(f"GENERATED_WRAPPER {mode} {out}")
