module IC74373 (
    input  [7:0] D,
    input        LE,
    input        OE_BAR
    output [7:0] Q
);
    reg [7:0] latch_reg;

    assign Q = OE_BAR? 8'bzzzzzzzz : latch_reg;

    always @(*) begin
        if (LE)
            latch_reg = D;
    end
endmodule