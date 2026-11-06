// New application-style RTL: bounded circular-buffer address translation.
// Deliberately independent of XOR-delay and Gray-code development examples.
module address_logic(input [4:0] addr_q, output [4:0] addr_mem);
  wire [5:0] plus_three = {1'b0, addr_q} + 6'd3;
  wire [5:0] wrapped = (plus_three >= 6'd24) ? (plus_three - 6'd24) : plus_three;
  assign addr_mem = wrapped[4:0];
endmodule
