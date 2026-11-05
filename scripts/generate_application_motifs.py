#!/usr/bin/env python3
"""Fixed gate-level address-generator motifs, analogous to real digital blocks.

Uses explicit Nangate45 cell instances so integrated and isolated logic are
identical and no synthesis ambiguity changes the logic. Different contexts
implement different functions; only decoder variants *within each context*
are functionally matched. These examples are not independent application RTL.
"""
import argparse
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("kind",choices=["binary_increment","gray_encode","gray_decode"])
p.add_argument("width",type=int,choices=[8,16])
p.add_argument("wrapper",type=Path)
p.add_argument("producer",type=Path)
a=p.parse_args()

gates=[]
if a.kind=="binary_increment":
 gates += [
  "INV_X1 u_not0 (.A(addr_q[0]),.ZN(addr_mem[0]));",
  "XOR2_X1 u_inc1 (.A(addr_q[1]),.B(addr_q[0]),.Z(addr_mem[1]));",
  "wire c2,c3,c4;",
  "AND2_X1 u_c2 (.A(addr_q[0]),.B(addr_q[1]),.ZN(c2));",
  "XOR2_X1 u_inc2 (.A(addr_q[2]),.B(c2),.Z(addr_mem[2]));",
  "AND2_X1 u_c3 (.A(c2),.B(addr_q[2]),.ZN(c3));",
  "XOR2_X1 u_inc3 (.A(addr_q[3]),.B(c3),.Z(addr_mem[3]));",
  "AND2_X1 u_c4 (.A(c3),.B(addr_q[3]),.ZN(c4));",
  "XOR2_X1 u_inc4 (.A(addr_q[4]),.B(c4),.Z(addr_mem[4]));",
 ]
elif a.kind=="gray_encode":
 gates.append("assign addr_mem[4] = addr_q[4];")
 for i in range(4):
  gates.append(f"XOR2_X1 u_gray{i} (.A(addr_q[{i+1}]),.B(addr_q[{i}]),.Z(addr_mem[{i}]));")
else:
 gates.append("assign addr_mem[4] = addr_q[4];")
 for i in range(3,-1,-1):
  gates.append(f"XOR2_X1 u_decode{i} (.A(addr_mem[{i+1}]),.B(addr_q[{i}]),.Z(addr_mem[{i}]));")
common=["wire [4:0] addr_q;","wire [4:0] addr_mem;"]
common += [f"DFF_X1 u_addrff_{i} (.CK(clk),.D(addr_in[{i}]),.Q(addr_q[{i}]));" for i in range(5)]
common += gates
wrapper=[
f"// Frozen address producer: {a.kind}",
"module integrated_top (input clk,input [4:0] addr_in,",
f" input [{a.width-1}:0] data_in,input write_enable,output [{a.width-1}:0] data_out);",
f"wire [{a.width-1}:0] mem_q;"
]+common+[f"RAM32x{a.width} u_ram (.clk(clk),.D(data_in),.Q(mem_q),.addr_rw(addr_mem),.we(write_enable));"]
wrapper += [f"DFF_X1 u_capture_{i} (.CK(clk),.D(mem_q[{i}]),.Q(data_out[{i}]));" for i in range(a.width)]
wrapper += ["endmodule"]
producer=[
f"// Isolated pre-placement address producer: {a.kind}",
"module producer_top (input clk,input [4:0] addr_in,output [4:0] addr_mem);",
"wire [4:0] addr_q;"
]+common[2:]+["endmodule"]
for dest,src in ((a.wrapper,wrapper),(a.producer,producer)):
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text("\n".join(src)+"\n")
print("PRODUCER_CREATED",a.kind,a.width)
