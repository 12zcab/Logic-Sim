module ttl_7485 (
    input wire pin_A0,       // Word A Input Bit 0 (Least Significant)
    input wire pin_A1,       // Word A Input Bit 1
    input wire pin_A2,       // Word A Input Bit 2
    input wire pin_A3,       // Word A Input Bit 3 (Most Significant)
    input wire pin_B0,       // Word B Input Bit 0 (Least Significant)
    input wire pin_B1,       // Word B Input Bit 1
    input wire pin_B2,       // Word B Input Bit 2
    input wire pin_B3,       // Word B Input Bit 3 (Most Significant)
    input wire pin_IA_LT_B,  // Cascading Expansion Input (A < B)
    input wire pin_IA_EQ_B,  // Cascading Expansion Input (A = B)
    input wire pin_IA_GT_B,  // Cascading Expansion Input (A > B)
    output reg pin_OA_LT_B,  // Comparator Terminal Output (A < B)
    output reg pin_OA_EQ_B,  // Comparator Terminal Output (A = B)
    output reg pin_OA_GT_B   // Comparator Terminal Output (A > B)
);

    wire [3:0] val_A;
    wire [3:0] val_B;

    assign val_A = {pin_A3, pin_A2, pin_A1, pin_A0};
    assign val_B = {pin_B3, pin_B2, pin_B1, pin_B0};

    always @(*) begin
        // Reset all processing flags to false status defaults
        pin_OA_LT_B = 1'b0;
        pin_OA_EQ_B = 1'b0;
        pin_OA_GT_B = 1'b0;

        if (val_A > val_B) begin
            pin_OA_GT_B = 1'b1;
        end else if (val_A < val_B) begin
            pin_OA_LT_B = 1'b1;
        end else begin
            // If the 4-bit words are exactly equal, look down to evaluate the expansion pins
            if (pin_IA_EQ_B == 1'b1) begin
                pin_OA_EQ_B = 1'b1;
                pin_OA_GT_B = pin_IA_GT_B;
                pin_OA_LT_B = pin_IA_LT_B;
            end else begin
                // Traditional 7485 cascade logic behavior overriding defaults
                pin_OA_GT_B = pin_IA_GT_B;
                pin_OA_LT_B = pin_IA_LT_B;
                pin_OA_EQ_B = 1'b0;
            end
        end
    end

endmodule