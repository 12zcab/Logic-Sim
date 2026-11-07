module sig_8T14 (
    input wire pin_1A,   // High-Capacitance Bus Input 1
    output reg pin_1Y,   // Shaped Inverted Output 1
    input wire pin_2A,   // High-Capacitance Bus Input 2
    output reg pin_2Y,   // Shaped Inverted Output 2
    input wire pin_3A,   // High-Capacitance Bus Input 3
    output reg pin_3Y    // Shaped Inverted Output 3
);

    always @(*) begin
        pin_1Y = ~pin_1A;
        pin_2Y = ~pin_2A;
        pin_3Y = ~pin_3A;
    end

endmodule