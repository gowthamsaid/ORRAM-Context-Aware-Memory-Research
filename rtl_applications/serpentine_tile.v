// Address remapping for alternating-direction tiled 2D scan.
// 4 logical rows x 8 columns encoded within the five-bit memory address.
module address_logic(input [4:0] addr_q, output [4:0] addr_mem);
  wire [1:0] row = addr_q[4:3];
  wire [2:0] column = addr_q[2:0];
  wire [2:0] selected_col = row[0] ? (3'd7 - column) : column;
  assign addr_mem = {row, selected_col};
endmodule
