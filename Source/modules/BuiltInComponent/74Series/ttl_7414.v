module ttl_7414 (
    input wire pin_1A,   // Schmitt Inverter 1 Input
    output reg pin_1Y,   // Schmitt Inverter 1 Output
    input wire pin_2A,   // Schmitt Inverter 2 Input
    output reg pin_2Y,   // Schmitt Inverter 2 Output
    input wire pin_3A,   // Schmitt Inverter 3 Input
    output reg pin_3Y,   // Schmitt Inverter 3 Output
    output reg pin_4Y,   // Schmitt Inverter 4 Output
    input wire pin_4A,   // Schmitt Inverter 4 Input
    output reg pin_5Y,   // Schmitt Inverter 5 Output
    input wire pin_5A,   // Schmitt Inverter 5 Input
    output reg pin_6Y,   // Schmitt Inverter 6 Output
    input wire pin_6A    // Schmitt Inverter 6 Input
);

    always @(*) begin
        pin_1Y = ~pin_1A;
        pin_2Y = ~pin_2A;
        pin_3Y = ~pin_3A;
        pin_4Y = ~pin_4A;
        pin_5Y = ~pin_5A;
        pin_6Y = ~pin_6A;
    end

endmodule