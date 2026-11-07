module intel_8253 (
    input wire pin_CS_BAR,    // Chip Select Line (Active-Low)
    input wire pin_RD_BAR,    // Processor Read Strobe Line (Active-Low)
    input wire pin_WR_BAR,    // Processor Write Strobe Line (Active-Low)
    input wire pin_A0,        // Register Select Address Line 0
    input wire pin_A1,        // Register Select Address Line 1
    input wire [7:0] pin_D,   // Host Microprocessor Parallel Data Access Bus
    input wire pin_CLK0,      // Timer Counter 0 Input Pulse Trigger
    input wire pin_GATE0,     // Timer Counter 0 Gate Control (High enables count)
    output reg pin_OUT0       // Timer Counter 0 Square Wave Output
);

    reg [15:0] count_register_0;
    reg [7:0]  control_register;
    reg [15:0] internal_decrementer_0;

    // Handle control instructions and target constant parameter values from host CPU
    always @(posedge pin_WR_BAR) begin
        if (!pin_CS_BAR) begin
            if ({pin_A1, pin_A0} == 2'b11) begin
                control_register <= pin_D;
            end else if ({pin_A1, pin_A0} == 2'b00) begin
                // Simplified 8-bit fallback loading for simulation environments
                count_register_0[7:0] <= pin_D;
                internal_decrementer_0[7:0] <= pin_D;
            end
        end
    end

    // Real-time tracking decrementer clock loop evaluation
    always @(posedge pin_CLK0) begin
        if (pin_GATE0) begin
            if (internal_decrementer_0 == 16'd0) begin
                internal_decrementer_0 <= count_register_0;
                pin_OUT0 <= ~pin_OUT0; // Toggle output to form balanced square waves
            end else begin
                internal_decrementer_0 <= internal_decrementer_0 - 16'd1;
            end
        end
    end

endmodule