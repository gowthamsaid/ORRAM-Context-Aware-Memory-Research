// Fixed-stride DMA ring index remapping; truncates modulo 32.
module address_logic(input [4:0] addr_q, output [4:0] addr_mem);
  wire [5:0] stride = {1'b0, addr_q} * 6'd3 + 6'd1;
  assign addr_mem = stride[4:0];
endmodule
