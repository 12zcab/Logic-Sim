module ttl_7476 (
    input wire pin_1CLK,     // Flip-Flop 1 Clock Input (Pulse-triggered / posedge)
    input wire pin_1J,       // Flip-Flop 1 J-Input
    input wire pin_1K,       // Flip-Flop 1 K-Input
    input wire pin_1CLR_BAR, // Flip-Flop 1 Clear Input (Active-Low)
    input wire pin_1PR_BAR,  // Flip-Flop 1 Preset Input (Active-Low)
    output reg pin_1Q,       // Flip-Flop 1 True Output
    output reg pin_1Q_BAR,   // Flip-Flop 1 Inverted Output
    input wire pin_2CLK,     // Flip-Flop 2 Clock Input (Pulse-triggered / posedge)
    input wire pin_2J,       // Flip-Flop 2 J-Input
    input wire pin_2K,       // Flip-Flop 2 K-Input
    input wire pin_2CLR_BAR, // Flip-Flop 2 Clear Input (Active-Low)
    input wire pin_2PR_BAR,  // Flip-Flop 2 Preset Input (Active-Low)
    output reg pin_2Q,       // Flip-Flop 2 True Output
    output reg pin_2Q_BAR    // Flip-Flop 2 Inverted Output
);

    // Flip-Flop 1 Core JK Logic
    always @(posedge pin_1CLK or negedge pin_1CLR_BAR or negedge pin_1PR_BAR) begin
        if (!pin_1CLR_BAR) begin
            pin_1Q     <= 1'b0;
            pin_1Q_BAR <= 1'b1;
        end else if (!pin_1PR_BAR) begin
            pin_1Q     <= 1'b1;
            pin_1Q_BAR <= 1'b0;
        end else begin
            case ({pin_1J, pin_1K})
                2'b00: begin pin_1Q <= pin_1Q; pin_1Q_BAR <= pin_1Q_BAR; end // Hold
                2'b01: begin pin_1Q <= 1'b0;   pin_1Q_BAR <= 1'b1;       end // Reset
                2'b10: begin pin_1Q <= 1'b1;   pin_1Q_BAR <= 1'b0;       end // Set
                2'b11: begin pin_1Q <= ~pin_1Q; pin_1Q_BAR <= ~pin_1Q_BAR; end // Toggle
            endcase
        end
    end

    // Flip-Flop 2 Core JK Logic
    always @(posedge pin_2CLK or negedge pin_2CLR_BAR or negedge pin_2PR_BAR) begin
        if (!pin_2CLR_BAR) begin
            pin_2Q     <= 1'b0;
            pin_2Q_BAR <= 1'b1;
        end else if (!pin_2PR_BAR) begin
            pin_2Q     <= 1'b1;
            pin_2Q_BAR <= 1'b0;
        end else begin
            case ({pin_2J, pin_2K})
                2'b00: begin pin_2Q <= pin_2Q; pin_2Q_BAR <= pin_2Q_BAR; end // Hold
                2'b01: begin pin_2Q <= 1'b0;   pin_2Q_BAR <= 1'b1;       end // Reset
                2'b10: begin pin_2Q <= 1'b1;   pin_2Q_BAR <= 1'b0;       end // Set
                2'b11: begin pin_2Q <= ~pin_2Q; pin_2Q_BAR <= ~pin_2Q_BAR; end // Toggle
            endcase
        end
    end

endmodule