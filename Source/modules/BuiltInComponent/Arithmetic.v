module ttl_7483 (
    input wire pin_A1,   // Operand A Bit 1 (Least Significant)
    input wire pin_A2,   // Operand A Bit 2
    input wire pin_A3,   // Operand A Bit 3
    input wire pin_A4,   // Operand A Bit 4 (Most Significant)
    input wire pin_B1,   // Operand B Bit 1 (Least Significant)
    input wire pin_B2,   // Operand B Bit 2
    input wire pin_B3,   // Operand B Bit 3
    input wire pin_B4,   // Operand B Bit 4 (Most Significant)
    input wire pin_C0,   // Carry-In Input
    output reg pin_S1,   // Sum Output Bit 1
    output reg pin_S2,   // Sum Output Bit 2
    output reg pin_S3,   // Sum Output Bit 3
    output reg pin_S4,   // Sum Output Bit 4
    output reg pin_C4    // Carry-Out Output Bit 4
);

    reg [4:0] sum_extended; // Temporary tracking array for handling carry overflow bit

    always @(*) begin
        sum_extended = {pin_A4, pin_A3, pin_A2, pin_A1} + {pin_B4, pin_B3, pin_B2, pin_B1} + pin_C0;
        
        pin_S1 = sum_extended;
        pin_S2 = sum_extended;
        pin_S3 = sum_extended;
        pin_S4 = sum_extended;
        pin_C4 = sum_extended; // Extra MSB represents total arithmetic carry out
    end

endmodule

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

module ttl_74181 (
    input wire pin_A0,       // Operand A Input Bit 0
    input wire pin_A1,       // Operand A Input Bit 1
    input wire pin_A2,       // Operand A Input Bit 2
    input wire pin_A3,       // Operand A Input Bit 3
    input wire pin_B0,       // Operand B Input Bit 0
    input wire pin_B1,       // Operand B Input Bit 1
    input wire pin_B2,       // Operand B Input Bit 2
    input wire pin_B3,       // Operand B Input Bit 3
    input wire pin_S0,       // Function Select Bit 0
    input wire pin_S1,       // Function Select Bit 1
    input wire pin_S2,       // Function Select Bit 2
    input wire pin_S3,       // Function Select Bit 3
    input wire pin_M,        // Mode Control Pin (High = Logic, Low = Arithmetic)
    input wire pin_CN_BAR,   // Ripple Carry Input (Active-Low)
    output reg pin_F0,       // ALU Output Function Bit 0
    output reg pin_F1,       // ALU Output Function Bit 1
    output reg pin_F2,       // ALU Output Function Bit 2
    output reg pin_F3,       // ALU Output Function Bit 3
    output reg pin_AEB,      // Equality Status Output (A Equals B indicator flag)
    output reg pin_G_BAR,    // Carry Generate Output (Active-Low)
    output reg pin_P_BAR,    // Carry Propagate Output (Active-Low)
    output reg pin_CN4_BAR   // Ripple Carry Output (Active-Low)
);

    wire [3:0] A;
    wire [3:0] B;
    wire [3:0] S;
    reg [4:0] F_ext; // Internal evaluation container matching logic steps plus carry flag
    wire cin;

    assign A   = {pin_A3, pin_A2, pin_A1, pin_A0};
    assign B   = {pin_B3, pin_B2, pin_B1, pin_B0};
    assign S   = {pin_S3, pin_S2, pin_S1, pin_S0};
    assign cin = !pin_CN_BAR; // Invert to process with standard high active mathematics inside matrix

    always @(*) begin
        if (pin_M) begin
            // --- LOGICAL OPERATIONS (Mode Pin M is High) ---
            F_ext = 5'b0;
            case (S)
                4'd0:  F_ext[3:0] = ~A;
                4'd1:  F_ext[3:0] = ~(A | B);
                4'd2:  F_ext[3:0] = (~A) & B;
                4'd3:  F_ext[3:0] = 4'b0000;
                4'd4:  F_ext[3:0] = ~(A & B);
                4'd5:  F_ext[3:0] = ~B;
                4'd6:  F_ext[3:0] = A ^ B;
                4'd7:  F_ext[3:0] = A & (~B);
                4'd8:  F_ext[3:0] = (~A) | B;
                4'd9:  F_ext[3:0] = ~(A ^ B);
                4'd10: F_ext[3:0] = B;
                4'd11: F_ext[3:0] = A & B;
                4'd12: F_ext[3:0] = 4'b1111;
                4'd13: F_ext[3:0] = A | (~B);
                4'd14: F_ext[3:0] = A | B;
                4'd15: F_ext[3:0] = A;
            endcase
            pin_CN4_BAR = 1'b1; // Carry line stays high (inactive) under pure logical configurations
        end else begin
            // --- ARITHMETIC OPERATIONS (Mode Pin M is Low) ---
            case (S)
                4'd0:  F_ext = A + cin;
                4'd1:  F_ext = (A | B) + cin;
                4'd2:  F_ext = (A | (~B)) + cin;
                4'd3:  F_ext = 5'b00000 - 1'b1 + cin; // Minus 1 representation
                4'd4:  F_ext = A + (A & (~B)) + cin;
                4'd5:  F_ext = (A | B) + (A & (~B)) + cin;
                4'd6:  F_ext = A - B - 1'b1 + cin;
                4'd7:  F_ext = (A & (~B)) - 1'b1 + cin;
                4'd8:  F_ext = A + (A & B) + cin;
                4'd9:  F_ext = A + B + cin;
                4'd10: F_ext = (A | (~B)) + (A & B) + cin;
                4'd11: F_ext = (A & B) - 1'b1 + cin;
                4'd12: F_ext = A + A + cin;
                4'd13: F_ext = (A | B) + A + cin;
                4'd14: F_ext = (A | (~B)) + A + cin;
                4'd15: F_ext = A - 1'b1 + cin;
            endcase
            pin_CN4_BAR = !F_ext[4]; // Extract final arithmetic position inversion
        end

        // Interface Bus Output Assignments
        pin_F0  = F_ext[0];
        pin_F1  = F_ext[1];
        pin_F2  = F_ext[2];
        pin_F3  = F_ext[3];
        pin_AEB = (F_ext[3:0] == 4'b1111); // Open-collector output active when function result passes all ones

        // Generate and Propagate terms for high-speed lookahead carry controllers
        pin_P_BAR = !((A | B) == 4'b1111);
        pin_G_BAR = !((A & B) != 4'b0000);
    end

endmodule