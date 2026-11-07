module ttl_7474 (
    input wire pin_1CLK,     // Flip-Flop 1 Clock Input (Active on posedge)
    input wire pin_1D,       // Flip-Flop 1 Data Input
    input wire pin_1CLR_BAR, // Flip-Flop 1 Clear Input (Active-Low)
    input wire pin_1PR_BAR,  // Flip-Flop 1 Preset Input (Active-Low)
    output reg pin_1Q,       // Flip-Flop 1 True Output
    output reg pin_1Q_BAR,   // Flip-Flop 1 Inverted Output
    input wire pin_2CLK,     // Flip-Flop 2 Clock Input (Active on posedge)
    input wire pin_2D,       // Flip-Flop 2 Data Input
    input wire pin_2CLR_BAR, // Flip-Flop 2 Clear Input (Active-Low)
    input wire pin_2PR_BAR,  // Flip-Flop 2 Preset Input (Active-Low)
    output reg pin_2Q,       // Flip-Flop 2 True Output
    output reg pin_2Q_BAR    // Flip-Flop 2 Inverted Output
);

    // Flip-Flop 1 Core Logic Loop
    always @(posedge pin_1CLK or negedge pin_1CLR_BAR or negedge pin_1PR_BAR) begin
        if (!pin_1CLR_BAR) begin
            pin_1Q     <= 1'b0;
            pin_1Q_BAR <= 1'b1;
        end else if (!pin_1PR_BAR) begin
            pin_1Q     <= 1'b1;
            pin_1Q_BAR <= 1'b0;
        end else begin
            pin_1Q     <= pin_1D;
            pin_1Q_BAR <= ~pin_1D;
        end
    end

    // Flip-Flop 2 Core Logic Loop
    always @(posedge pin_2CLK or negedge pin_2CLR_BAR or negedge pin_2PR_BAR) begin
        if (!pin_2CLR_BAR) begin
            pin_2Q     <= 1'b0;
            pin_2Q_BAR <= 1'b1;
        end else if (!pin_2PR_BAR) begin
            pin_2Q     <= 1'b1;
            pin_2Q_BAR <= 1'b0;
        end else begin
            pin_2Q     <= pin_2D;
            pin_2Q_BAR <= ~pin_2D;
        end
    end

endmodule