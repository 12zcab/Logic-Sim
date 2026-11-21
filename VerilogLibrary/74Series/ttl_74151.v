module IC74151 (
    input  [7:0] D,
    input  [2:0] S,
    input        E_BAR
    output       Y,
    output       W
);
    assign Y = E_BAR? 1'b0 : D[S];
    assign W = E_BAR? 1'b1 : ~D[S];
endmodule