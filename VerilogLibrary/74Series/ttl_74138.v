module IC74138 (
    input  [2:0] A,
    input        G1,
    input        G2A_BAR
    input        G2B_BAR
    output [7:0] Y_n
);
    wire en = G1 & ~G2A_BAR& ~G2B_n;
    assign Y_BAR= en ? ~(8'b00000001 << A) : 8'b11111111;
endmodule