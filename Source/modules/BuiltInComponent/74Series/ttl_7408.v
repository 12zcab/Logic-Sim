module ttl_7408 (
    input wire 1A,       // Gate 1 Input A
    input wire 1B,       // Gate 1 Input B
    output reg 1Y,       // Gate 1 Output Y
    input wire 2A,       // Gate 2 Input A
    input wire 2B,       // Gate 2 Input B
    output reg 2Y,       // Gate 2 Output Y
    input wire 3A,       // Gate 3 Input A
    input wire 3B,       // Gate 3 Input B
    output reg 3Y,       // Gate 3 Output Y
    input wire 4A,       // Gate 4 Input A
    input wire 4B,       // Gate 4 Input B
    output reg 4Y        // Gate 4 Output Y
);

    always @(*) begin
        1Y = 1A & 1B;
        2Y = 2A & 2B;
        3Y = 3A & 3B;
        4Y = 4A & 4B;
    end

endmodule