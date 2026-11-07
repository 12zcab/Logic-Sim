module ttl_7486 (
    input wire pin_1A,   // Gate 1 Input A
    input wire pin_1B,   // Gate 1 Input B
    output reg pin_1Y,   // Gate 1 Output Y
    input wire pin_2A,   // Gate 2 Input A
    input wire pin_2B,   // Gate 2 Input B
    output reg pin_2Y,   // Gate 2 Output Y
    input wire pin_3A,   // Gate 3 Input A
    input wire pin_3B,   // Gate 3 Input B
    output reg pin_3Y,   // Gate 3 Output Y
    input wire pin_4A,   // Gate 4 Input A
    input wire pin_4B,   // Gate 4 Input B
    output reg pin_4Y    // Gate 4 Output Y
);

    always @(*) begin
        pin_1Y = pin_1A ^ pin_1B;
        pin_2Y = pin_2A ^ pin_2B;
        pin_3Y = pin_3A ^ pin_3B;
        pin_4Y = pin_4A ^ pin_4B;
    end

endmodule