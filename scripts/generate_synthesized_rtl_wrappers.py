#!/usr/bin/env python3
"""Instantiate a *mapped* synthesizable address-logic module in matching wrappers.

The original behavioral RTL is separately synthesized with Yosys/ABC.
This script does not generate gate equations or select an architecture.
The mapping is bit-for-bit the same in the isolated producer and the
registered memory integration, for both row and word candidates.
"""
import argparse
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("name",choices=("ring24","serpentine_tile","dma_stride"))
p.add_argument("width",type=int,choices=(8,16))
p.add_argument("dest",type=Path)
p.add_argument("producer_dest",type=Path)
a=p.parse_args()
n=a.width
common=[
  "wire [4:0] addr_q;",
  "wire [4:0] addr_mem;",
  *[f"DFF_X1 u_addrff_{i} (.CK(clk), .D(addr_in[{i}]), .Q(addr_q[{i}]));" for i in range(5)],
  "address_logic u_addr_gen (.addr_q(addr_q), .addr_mem(addr_mem));"
]
wrapper=[
 f"// Synthesized RTL address generator: {a.name}. Matched across decoder variants.",
 "module integrated_top (input clk, input [4:0] addr_in,",
 f" input [{n-1}:0] data_in,input write_enable,output [{n-1}:0] data_out);",
 f"wire [{n-1}:0] mem_q;", *common,
 f"RAM32x{n} u_ram (.clk(clk), .D(data_in), .Q(mem_q), .addr_rw(addr_mem), .we(write_enable));",
 *[f"DFF_X1 u_capture_{i} (.CK(clk), .D(mem_q[{i}]), .Q(data_out[{i}]));" for i in range(n)],
 "endmodule"
]
producer=[
 f"// Same synthesized mapped address_logic; independent of RAM placement.",
 "module producer_top (input clk,input [4:0] addr_in,output [4:0] addr_mem);",
 "wire [4:0] addr_q;",
 *[f"DFF_X1 u_addrff_{i} (.CK(clk), .D(addr_in[{i}]), .Q(addr_q[{i}]));" for i in range(5)],
 "address_logic u_addr_gen (.addr_q(addr_q), .addr_mem(addr_mem));",
 "endmodule"
]
for dest,lines in ((a.dest,wrapper),(a.producer_dest,producer)):
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text("\n".join(lines)+"\n")
print("MAPPED_WRAPPERS_READY",a.name,n)
