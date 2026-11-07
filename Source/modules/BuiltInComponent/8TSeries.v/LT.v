module sig_8T23 (
    input wire pin_1A,   // Standard 5V TTL Logic Input 1
    output reg pin_1Y,   // High-Swing Shifted Output 1
    input wire pin_2A,   // Standard 5V TTL Logic Input 2
    output reg pin_2Y    // High-Swing Shifted Output 2
);

    always @(*) begin
        pin_1Y = pin_1A; // Maintains logical matching properties while crossing electrical domains
        pin_2Y = pin_2A;
    end

endmodule

module sig_8T24 (
    input wire pin_1A,   // High-Voltage MOS System Input 1
    output reg pin_1Y,   // Standard 5V TTL Shifted Output 1
    input wire pin_2A,   // High-Voltage MOS System Input 2
    output reg pin_2Y    // Standard 5V TTL Shifted Output 2
);

    always @(*) begin
        pin_1Y = pin_1A; 
        pin_2Y = pin_2A;
    end

endmodule
