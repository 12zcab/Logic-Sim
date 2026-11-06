module ttl_7400 (
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
        1Y = ~(1A & 1B);
        2Y = ~(2A & 2B);
        3Y = ~(3A & 3B);
        4Y = ~(4A & 4B);
    end
    

endmodule

module ttl_7404 (
    input wire 1A,       // Inverter 1 Input
    output reg 1Y,       // Inverter 1 Output
    input wire 2A,       // Inverter 2 Input
    output reg 2Y,       // Inverter 2 Output
    input wire 3A,       // Inverter 3 Input
    output reg 3Y,       // Inverter 3 Output
    input wire 4A,       // Inverter 4 Input
    output reg 4Y,       // Inverter 4 Output
    input wire 5A,       // Inverter 5 Input
    output reg 5Y,       // Inverter 5 Output
    input wire 6A,       // Inverter 6 Input
    output reg 6Y        // Inverter 6 Output
);

    always @(*) begin
        1Y = ~1A;
        2Y = ~2A;
        3Y = ~3A;
        4Y = ~4A;
        5Y = ~5A;
        6Y = ~6A;
    end

endmodule

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

module ttl_7432 (
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
        pin_1Y = pin_1A | pin_1B;
        pin_2Y = pin_2A | pin_2B;
        pin_3Y = pin_3A | pin_3B;
        pin_4Y = pin_4A | pin_4B;
    end

endmodule

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

module ttl_7432 (
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
        pin_1Y = pin_1A | pin_1B;
        pin_2Y = pin_2A | pin_2B;
        pin_3Y = pin_3A | pin_3B;
        pin_4Y = pin_4A | pin_4B;
    end

endmodule

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

module ttl_7430 (
    input wire pin_A,    // Input Channel A
    input wire pin_B,    // Input Channel B
    input wire pin_C,    // Input Channel C
    input wire pin_D,    // Input Channel D
    input wire pin_E,    // Input Channel E
    input wire pin_F,    // Input Channel F
    input wire pin_G,    // Input Channel G
    input wire pin_H,    // Input Channel H
    output reg pin_Y     // Unified NAND Output Y
);

    always @(*) begin
        pin_Y = ~(pin_A & pin_B & pin_C & pin_D & pin_E & pin_F & pin_G & pin_H);
    end

endmodule

