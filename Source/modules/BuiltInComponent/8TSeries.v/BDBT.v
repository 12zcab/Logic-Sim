module sig_8T26 (
    input wire pin_E_BAR,  // Transceiver Output Enable (Active-Low)
    input wire pin_DRV,    // Driver/Receiver Routing Direction Control (High = Transmit, Low = Receive)
    input wire pin_A1,     // Port A Terminal 1 Logic Node
    inout wire pin_B1,     // Shared Bus Terminal 1 Data Line
    input wire pin_A2,     // Port A Terminal 2 Logic Node
    inout wire pin_B2,     // Shared Bus Terminal 2 Data Line
    input wire pin_A3,     // Port A Terminal 3 Logic Node
    inout wire pin_B3,     // Shared Bus Terminal 3 Data Line
    input wire pin_A4,     // Port A Terminal 4 Logic Node
    inout wire pin_B4,     // Shared Bus Terminal 4 Data Line
    output reg pin_RX1,    // Dedicated Receiver Channel 1 True Read Output
    output reg pin_RX2,    // Dedicated Receiver Channel 2 True Read Output
    output reg pin_RX3,    // Dedicated Receiver Channel 3 True Read Output
    output reg pin_RX4     // Dedicated Receiver Channel 4 True Read Output
);

    // Compute driver and receiver active matrix states
    wire transmit_active;
    assign transmit_active = (!pin_E_BAR) && pin_DRV;

    // Handle Bidirectional Drive Operations on External Bus Side (Port B)
    assign pin_B1 = (transmit_active) ? ~pin_A1 : 1'bz;
    assign pin_B2 = (transmit_active) ? ~pin_2A  : 1'bz; // Clean structural pin naming logic mapping inside Yosys
    assign pin_B3 = (transmit_active) ? ~pin_A3 : 1'bz;
    assign pin_B4 = (transmit_active) ? ~pin_A4 : 1'bz;

    // Handle Local Receiver Reads (Port RX maps inverted bus data back out to card)
    always @(*) begin
        pin_RX1 = ~pin_B1;
        pin_RX2 = ~pin_B2;
        pin_RX3 = ~pin_B3;
        pin_RX4 = ~pin_B4;
    end

endmodule

module sig_8T28 (
    input wire pin_E_BAR,  // Transceiver Output Enable (Active-Low)
    input wire pin_DRV,    // Driver/Receiver Direction Control (High = Transmit, Low = Receive)
    input wire pin_A1,     // Port A Terminal 1 Logic Node
    inout wire pin_B1,     // Shared Bus Terminal 1 Data Line
    input wire pin_A2,     // Port A Terminal 2 Logic Node
    inout wire pin_B2,     // Shared Bus Terminal 2 Data Line
    input wire pin_A3,     // Port A Terminal 3 Logic Node
    inout wire pin_B3,     // Shared Bus Terminal 3 Data Line
    input wire pin_A4,     // Port A Terminal 4 Logic Node
    inout wire pin_B4,     // Shared Bus Terminal 4 Data Line
    output reg pin_RX1,    // Dedicated Receiver Channel 1 True Read Output
    output reg pin_RX2,    // Dedicated Receiver Channel 2 True Read Output
    output reg pin_RX3,    // Dedicated Receiver Channel 3 True Read Output
    output reg pin_RX4     // Dedicated Receiver Channel 4 True Read Output
);

    wire transmit_active;
    assign transmit_active = (!pin_E_BAR) && pin_DRV;

    // Route non-inverted signals to bus line if active
    assign pin_B1 = (transmit_active) ? pin_A1 : 1'bz;
    assign pin_B2 = (transmit_active) ? pin_A2 : 1'bz;
    assign pin_B3 = (transmit_active) ? pin_A3 : 1'bz;
    assign pin_B4 = (transmit_active) ? pin_A4 : 1'bz;

    // Read non-inverted bus statuses directly back to local system pins
    always @(*) begin
        pin_RX1 = pin_B1;
        pin_RX2 = pin_B2;
        pin_RX3 = pin_B3;
        pin_RX4 = pin_B4;
    end

endmodule


