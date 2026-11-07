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