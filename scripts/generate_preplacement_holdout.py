#!/usr/bin/env python3
"""Deterministic XOR-address holdout wrappers; matched row/word RTL per case.

Architecture-invariant connected logic, deliberately crafted stress cases.
No physical results or winner labels are consulted by this generator.
"""
import argparse
from pathlib import Path

PROFILES = {
    "balanced": [1, 1, 1, 1, 1],  # calibration
    "late_low": [3, 3, 1, 1, 1],  # previous test, NOT new holdout
    "late_high": [1, 1, 1, 3, 3],  # new locked holdout
    "late_mid": [1, 1, 3, 1, 1],   # new locked holdout
    "staggered": [2, 1, 3, 1, 2],  # new locked holdout
}
parser = argparse.ArgumentParser()
parser.add_argument("context", choices=PROFILES.keys())
parser.add_argument("word_size", type=int, choices=(8, 16, 32))
parser.add_argument("dest", type=Path)
args = parser.parse_args()
d = PROFILES[args.context]
n = args.word_size
src = [
    f"// context {args.context}, XOR stage depths {d}, word_size {n}",
    "module integrated_top(input clk, input [4:0] addr_in,",
    f"input [{n-1}:0] data_in, input write_enable, output [{n-1}:0] data_out);",
    "wire [4:0] addr_q;",
    "wire [4:0] addr_mem;",
    f"wire [{n-1}:0] mem_q;",
]
for i in range(5):
    src.append(f"DFF_X1 u_addrff_{i} (.CK(clk), .D(addr_in[{i}]), .Q(addr_q[{i}]));")
for i in range(5):
    previous = f"addr_q[{i}]"
    for j in range(d[i]):
        target = f"addr_mem[{i}]" if j == d[i]-1 else f"logic_{i}_{j}"
        if j < d[i]-1:
            src.append(f"wire {target};")
        other = f"addr_q[{(i+j+1)%5}]"
        src.append(f"XOR2_X1 u_mix_{i}_{j} (.A({previous}), .B({other}), .Z({target}));")
        previous = target
src.append(f"RAM32x{n} u_ram (.clk(clk), .D(data_in), .Q(mem_q), .addr_rw(addr_mem), .we(write_enable));")
for i in range(n):
    src.append(f"DFF_X1 u_capture_{i} (.CK(clk), .D(mem_q[{i}]), .Q(data_out[{i}]));")
src.append("endmodule")
args.dest.parent.mkdir(parents=True, exist_ok=True)
args.dest.write_text("\n".join(src) + "\n")
print(f"GENERATED context={args.context} width={n} depths={d}")
