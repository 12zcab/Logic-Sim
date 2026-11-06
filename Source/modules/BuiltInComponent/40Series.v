module cmos_4011 (
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

module cmos_4013 (
    input wire 1CLK,     // Flip-Flop 1 Clock
    input wire 1D,       // Flip-Flop 1 Data Input
    input wire 1SET,     // Flip-Flop 1 Asynchronous Set (Active-High)
    input wire 1RST,     // Flip-Flop 1 Asynchronous Reset (Active-High)
    output reg 1Q,       // Flip-Flop 1 True Output
    output reg 1Q_BAR,   // Flip-Flop 1 Inverted Output
    input wire 2CLK,     // Flip-Flop 2 Clock
    input wire 2D,       // Flip-Flop 2 Data Input
    input wire 2SET,     // Flip-Flop 2 Asynchronous Set (Active-High)
    input wire 2RST,     // Flip-Flop 2 Asynchronous Reset (Active-High)
    output reg 2Q,       // Flip-Flop 2 True Output
    output reg 2Q_BAR    // Flip-Flop 2 Inverted Output
);

    // Flip-Flop 1 Structural Logic Matrix
    always @(posedge 1CLK or posedge 1SET or posedge 1RST) begin
        if (1RST) begin
            1Q     <= 1'b0;
            1Q_BAR <= 1'b1;
        end else if (1SET) begin
            1Q     <= 1'b1;
            1Q_BAR <= 1'b0;
        end else begin
            1Q     <= 1D;
            1Q_BAR <= ~1D;
        end
    end

    // Flip-Flop 2 Structural Logic Matrix
    always @(posedge 2CLK or posedge 2SET or posedge 2RST) begin
        if (2RST) begin
            2Q     <= 1'b0;
            2Q_BAR <= 1'b1;
        end else if (2SET) begin
            2Q     <= 1'b1;
            2Q_BAR <= 1'b0;
        end else begin
            2Q     <= 2D;
            2Q_BAR <= ~2D;
        end
    end

endmodule

module cmos_4017 (
    input wire CLK,      // Clock Input
    input wire CLK_EN,   // Clock Enable Input (Active-Low)
    input wire RESET,    // Asynchronous Reset Input (Active-High)
    output reg Q0,       // Counter Output Sequence 0
    output reg Q1,       // Counter Output Sequence 1
    output reg Q2,       // Counter Output Sequence 2
    output reg Q3,       // Counter Output Sequence 3
    output reg Q4,       // Counter Output Sequence 4
    output reg Q5,       // Counter Output Sequence 5
    output reg Q6,       // Counter Output Sequence 6
    output reg Q7,       // Counter Output Sequence 7
    output reg Q8,       // Counter Output Sequence 8
    output reg Q9,       // Counter Output Sequence 9
    output reg CO        // Carry Out Output (Divided-by-10 clock segment)
);

    reg [3:0] count;    // Internal sequence pointer register

    always @(posedge CLK or posedge RESET) begin
        if (RESET) begin
            count <= 4'd0;
        end else if (!CLK_EN) begin
            if (count >= 4'd9) begin
                count <= 4'd0;
            end else begin
                count <= count + 4'd1;
            end
        end
    end

    // Combinational Decoding matrix mapping sequencer back to output pins
    always @(*) begin
        Q0 = (count == 4'd0);
        Q1 = (count == 4'd1);
        Q2 = (count == 4'd2);
        Q3 = (count == 4'd3);
        Q4 = (count == 4'd4);
        Q5 = (count == 4'd5);
        Q6 = (count == 4'd6);
        Q7 = (count == 4'd7);
        Q8 = (count == 4'd8);
        Q9 = (count == 4'd9);
        CO = (count < 4'd5); // High for steps 0-4, Low for steps 5-9
    end

endmodule

module cmos_4066 (
    input wire 1A,       // Switch 1 Terminal A (Input/Output data path)
    input wire 1CONT,    // Switch 1 Control Pin (Active-High to close switch)
    output reg 1B,       // Switch 1 Terminal B (Input/Output data path)
    input wire 2A,       // Switch 2 Terminal A (Input/Output data path)
    input wire 2CONT,    // Switch 2 Control Pin (Active-High to close switch)
    output reg 2B,       // Switch 2 Terminal B (Input/Output data path)
    input wire 3A,       // Switch 3 Terminal A (Input/Output data path)
    input wire 3CONT,    // Switch 3 Control Pin (Active-High to close switch)
    output reg 3B,       // Switch 3 Terminal B (Input/Output data path)
    input wire 4A,       // Switch 4 Terminal A (Input/Output data path)
    input wire 4CONT,    // Switch 4 Control Pin (Active-High to close switch)
    output reg 4B        // Switch 4 Terminal B (Input/Output data path)
);

    // Pure digital behavioral representation of the transmission pass-gates
    always @(*) begin
        1B = (1CONT) ? 1A : 1'bz; // Passes data if closed, otherwise High-Impedance (Disconnected)
        2B = (2CONT) ? 2A : 1'bz; // Passes data if closed, otherwise High-Impedance (Disconnected)
        3B = (3CONT) ? 3A : 1'bz; // Passes data if closed, otherwise High-Impedance (Disconnected)
        4B = (4CONT) ? 4A : 1'bz; // Passes data if closed, otherwise High-Impedance (Disconnected)
    end

endmodule
