module IC74157 (
    input  [3:0] A,
    input  [3:0] B,
    input        S,
    input        G_BAR
    output [3:0] Y
);
    assign Y = G_BAR? 4'b0000 : (S ? B : A);
endmodule