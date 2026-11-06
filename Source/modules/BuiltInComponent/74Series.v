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

module ttl_7474 (
    input wire 1CLK,     // Flip-Flop 1 Clock
    input wire 1D,       // Flip-Flop 1 Data Input
    input wire 1CLR,     // Flip-Flop 1 Clear (Active-Low Reset)
    input wire 1PR,      // Flip-Flop 1 Preset (Active-Low Set)
    output reg 1Q,       // Flip-Flop 1 Direct Output
    output reg 1Q_BAR,   // Flip-Flop 1 Inverted Output
    input wire 2CLK,     // Flip-Flop 2 Clock
    input wire 2D,       // Flip-Flop 2 Data Input
    input wire 2CLR,     // Flip-Flop 2 Clear (Active-Low Reset)
    input wire 2PR,      // Flip-Flop 2 Preset (Active-Low Set)
    output reg 2Q,       // Flip-Flop 2 Direct Output
    output reg 2Q_BAR    // Flip-Flop 2 Inverted Output
);

    // Flip-Flop 1 Logic
    always @(posedge 1CLK or negedge 1CLR or negedge 1PR) begin
        if (!1CLR) begin
            1Q     <= 1'b0;
            1Q_BAR <= 1'b1;
        end else if (!1PR) begin
            1Q     <= 1'b1;
            1Q_BAR <= 1'b0;
        end else begin
            1Q     <= 1'D;
            1Q_BAR <= ~1'D;
        end
    end

    // Flip-Flop 2 Logic
    always @(posedge 2CLK or negedge 2CLR or negedge 2PR) begin
        if (!2CLR) begin
            2Q     <= 1'b0;
            2Q_BAR <= 1'b1;
        end else if (!2PR) begin
            2Q     <= 1'b1;
            2Q_BAR <= 1'b0;
        end else begin
            2Q     <= 2'D;
            2Q_BAR <= ~2'D;
        end
    end

endmodule

