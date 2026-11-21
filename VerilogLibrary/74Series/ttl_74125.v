module IC74125 (
    input  [3:0] A,
    input  [3:0] OE_BAR
    output [3:0] Y
);
    assign Y = OE_BAR? 1'bz : A;
    assign Y = OE_BAR? 1'bz : A;
    assign Y = OE_BAR? 1'bz : A;
    assign Y = OE_BAR? 1'bz : A;
endmodule