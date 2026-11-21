module IC74153 (
    input  [3:0] I1,
    input  [3:0] I2,
    input  [1:0] S,
    input        E1_BAR,
    input        E2_BAR,
    output       Y1,
    output       Y2
);
    assign Y1 = E1_BAR ? 1'b0 : I1[S];
    assign Y2 = E2_BAR ? 1'b0 : I2[S];
endmodule