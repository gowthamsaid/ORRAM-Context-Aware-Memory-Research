'timescale 1ns/1ps
module tb;
  reg clk=0;
  reg [7:0] D;
  reg [4:0] addr_rw;
  reg [0:0] we;
  wire [7:0] Q;
  reg [7:0] golden[0:31];
  integer i, a, v;
  RAM32x8 dut(.clk(clk), .D(D), .Q(Q), .addr_rw(addr_rw), .we(we));
  task write_word;
    input integer idx;
    input integer value;
    begin
      clk=0; addr_rw=idx; D=value; we=1; #2;
      clk=1; golden[idx]=value; #2;
      if (Q !== golden[idx]) $fatal(1,"write mismatch addr=%0d got=%0h expected=%0h",idx,Q,golden[idx]);
      clk=0; we=0; #2;
    end
  endtask
  initial begin
    D=0; addr_rw=0; we=0;
    for(i=0;i<32;i=i+1) write_word(i,(i*19+7)&255);
    for(i=0;i<32;i=i+1) begin
      addr_rw=i; #2;
      if (Q !== golden[i]) $fatal(1,"read mismatch addr=%0d got=%0h expected=%0h",i,Q,golden[i]);
    end
    for(i=0;i<128;i=i+1) begin
      a=(i*17+13)%32;v=(i*29+83)%256;
      if ((i%3)==0) write_word(a,v);
      else begin addr_rw=a;we=0;#2;if(Q!==golden[a]) $fatal(1,"random read mismatch i=%0d",i);end
    end
    $display("BEHAVIORAL_PASS RAM32x8");
    $finish;
  end
endmodule