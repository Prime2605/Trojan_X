//============================================================================
// PS13 Hardware Security — Trojan-Infected 8-bit ALU
//============================================================================
// Module:  trojan_alu8
// Purpose: ALU with injected hardware Trojans for benchmark validation.
//          Same interface as alu8.v — drop-in replacement.
//
// BENCHMARK PROGRESSION:
//
//   T1 → T2 → T3
//   ──────────────
//   T1: Prove the pipeline (basic combinational Trojan)
//   T2: Prove robustness (complex combinational — NOT YET IMPLEMENTED)
//   T3: Prove sequential capability (sequential/state — NOT YET IMPLEMENTED)
//
// SCA/timing is NOT T4 — it is a parallel analysis dimension applied to
// all three benchmarks.
//
//============================================================================
// T1: RARE-COMBINATION COMBINATIONAL TROJAN
//============================================================================
//
//   Model:  Digital, combinationally triggered, rare-condition HW Trojan
//   Ref:    Trust-Hub standard Trojan taxonomy (trigger + payload)
//
//   TRIGGER:
//     Uses specific bit positions from LEGITIMATE ALU signals (A, B, OP),
//     not arbitrary magic constants. The trigger is a rare combination of
//     bit-level conditions that is unlikely under normal operation but can
//     be activated in simulation and demonstrated on the Nexys A7.
//
//     Condition: A[7] & A[6] & ~A[5] & B[7] & ~B[6] & B[5] & OP[2]
//
//     This requires:
//       - A[7:5] = 3'b110  (A in range 0xC0-0xDF)
//       - B[7:5] = 3'b101  (B in range 0xA0-0xBF)
//       - OP[2]  = 1       (XOR, NOT, INC, or DEC operation)
//     Probability ≈ (1/8) × (1/8) × (1/2) = 1/128 per random input
//     (rare enough to evade casual testing, common enough to demonstrate)
//
//     Example trigger activation:
//       A = 8'hC0, B = 8'hA0, OP = 3'b100 (XOR)  → TRIGGERS
//       A = 8'hDF, B = 8'hBF, OP = 3'b110 (INC)  → TRIGGERS
//       A = 8'hC0, B = 8'hA0, OP = 3'b000 (ADD)  → does NOT trigger
//
//   PAYLOAD:
//     When trigger is active, XOR-flip bit [3] of ALU result.
//     This is a deliberately SMALL payload — a single-bit corruption —
//     so the analyzer can later ask:
//       "Where is the trigger?" → the AND-tree feeding t1_trigger
//       "Where is the payload?" → the XOR/MUX on Y[3]
//       "Which output is affected?" → Y[3]
//
//     After Vivado synthesis, the trigger becomes an AND-tree of LUTs,
//     and the payload becomes a MUX/XOR on the output path. The analyzer
//     must find these structures from the gate-level netlist alone.
//
//   STRUCTURAL SIGNATURE (post-synthesis, approximate):
//
//     A[7] ─┐
//     A[6] ─┤
//    ~A[5] ─┤
//     B[7] ─┼──► LUT (trigger AND-tree) ──► t1_trigger
//    ~B[6] ─┤                                    │
//     B[5] ─┤                                    ▼
//     OP[2] ┘                                ┌───────┐
//                                            │  MUX  │──► Y[3]
//                            alu_y[3] ──────►│       │
//                            alu_y[3]^1 ────►└───────┘
//
//============================================================================
// T2: COMPLEX COMBINATIONAL TROJAN — PLANNED, NOT YET IMPLEMENTED
//============================================================================
//   Will use a deeper, wider trigger cone with multi-level LUT chains.
//   Purpose: prove analyzer generalizes beyond T1's simple AND-tree.
//   Implementation order: after T1 pipeline is complete.
//
//============================================================================
// T3: SEQUENTIAL TROJAN — PLANNED, NOT YET IMPLEMENTED
//============================================================================
//   Will use FFs / counter / FSM for state-based trigger.
//   Purpose: prove analyzer can identify sequential security-sensitive
//   structures (FFs, clock connectivity, state paths).
//   Implementation order: after T2.
//
//============================================================================

// === Trojan Enable Switch ===
// Uncomment one of the following to inject a Trojan
`define ENABLE_T1
// `define ENABLE_T4

module trojan_alu8 (
    input  wire        clk,       // Clock (for T3 sequential — unused by T1)
    input  wire        rst_n,     // Active-low reset (for T3 — unused by T1)
    input  wire [7:0]  A,         // Operand A
    input  wire [7:0]  B,         // Operand B
    input  wire [2:0]  OP,        // Operation select
    output wire [7:0]  Y,         // Result
    output wire        carry,     // Carry flag
    output wire        zero,      // Zero flag
    output wire        overflow,  // Overflow flag
    input  wire        BTNC,      // Button Center (for T4)
    input  wire        BTND       // Button Down (for T4)
);

    //------------------------------------------------------------------------
    // Clean ALU core — identical logic to alu8.v
    //------------------------------------------------------------------------
    reg [7:0] alu_y;
    reg       alu_carry;
    reg       alu_zero;
    reg       alu_overflow;
    reg [8:0] result_wide;

    always @(*) begin
        result_wide  = 9'b0;
        alu_y        = 8'b0;
        alu_carry    = 1'b0;
        alu_zero     = 1'b0;
        alu_overflow = 1'b0;

        case (OP)
            3'b000: begin // ADD
                result_wide  = {1'b0, A} + {1'b0, B};
                alu_y        = result_wide[7:0];
                alu_carry    = result_wide[8];
                alu_overflow = (A[7] == B[7]) && (alu_y[7] != A[7]);
            end
            3'b001: begin // SUB
                result_wide  = {1'b0, A} - {1'b0, B};
                alu_y        = result_wide[7:0];
                alu_carry    = result_wide[8];
                alu_overflow = (A[7] != B[7]) && (alu_y[7] != A[7]);
            end
            3'b010: alu_y = A & B;   // AND
            3'b011: alu_y = A | B;   // OR
            3'b100: alu_y = A ^ B;   // XOR
            3'b101: alu_y = ~A;      // NOT
            3'b110: begin // INC
                result_wide  = {1'b0, A} + 9'b1;
                alu_y        = result_wide[7:0];
                alu_carry    = result_wide[8];
                alu_overflow = (~A[7]) && (alu_y[7]);
            end
            3'b111: begin // DEC
                result_wide  = {1'b0, A} - 9'b1;
                alu_y        = result_wide[7:0];
                alu_carry    = result_wide[8];
                alu_overflow = (A[7]) && (~alu_y[7]);
            end
            default: alu_y = 8'b0;
        endcase

        alu_zero = (alu_y == 8'b0);
    end

    //========================================================================
    // T1: COMBINATIONAL TROJAN — TRIGGER CODE "11" (BTNC + BTND)
    //========================================================================
    `ifdef ENABLE_T1

        //--------------------------------------------------------------------
        // TRIGGER: Both BTNC and BTND pressed simultaneously
        //
        // Trigger Code: 11  (BTNC=1, BTND=1)
        // On the Nexys A7 board, press BTNC (center) and BTND (down)
        // at the same time to activate the trojan.
        //--------------------------------------------------------------------
        wire t1_trigger = BTNC & BTND;

        //--------------------------------------------------------------------
        // PAYLOAD: XOR result with operand A
        //
        // When trigger is inactive: Y = alu_y          (correct output)
        // When trigger is active:   Y = alu_y ^ A      (corrupted output)
        //
        // This produces unpredictable-looking results because the
        // corruption depends on whatever value A currently holds.
        // Different inputs → different corruption every time.
        //--------------------------------------------------------------------
        assign Y        = t1_trigger ? (alu_y ^ A) : alu_y;       // PAYLOAD
        assign carry    = t1_trigger ? ~alu_carry  : alu_carry;    // Flip carry
        assign zero     = (Y == 8'b0);
        assign overflow = alu_overflow;

    //========================================================================
    // T2: COMPLEX COMBINATIONAL TROJAN
    //========================================================================
    `elsif ENABLE_T2

        //--------------------------------------------------------------------
        // TRIGGER: A[7:4] == 0xF AND B[7:4] == 0x0 AND OP == ADD
        // Stage 1: (A[7:4] == 4'hF) & (B[7:4] == 4'h0)
        // Stage 2: (OP == 3'b000)
        //--------------------------------------------------------------------
        wire t2_cond1 = (A[7:4] == 4'hF) & (B[7:4] == 4'h0);
        wire t2_cond2 = (OP == 3'b000);
        wire t2_trigger = t2_cond1 & t2_cond2;

        //--------------------------------------------------------------------
        // PAYLOAD: Force Y to 0x00, force carry to 1
        //--------------------------------------------------------------------
        assign Y        = t2_trigger ? 8'h00 : alu_y;
        assign carry    = t2_trigger ? 1'b1  : alu_carry;
        assign zero     = (Y == 8'b0); // Recalculate zero based on modified Y
        assign overflow = alu_overflow;

    //========================================================================
    // T3: SEQUENTIAL TROJAN
    //========================================================================
    `elsif ENABLE_T3

        //--------------------------------------------------------------------
        // TRIGGER: 4-bit counter-based sequential trigger
        // Condition: (A == 8'hFF) & (OP == 3'b111) observed >= 8 times
        //--------------------------------------------------------------------
        reg [3:0] trigger_count;
        wire rare_event = (A == 8'hFF) & (OP == 3'b111);

        always @(posedge clk or negedge rst_n) begin
            if (!rst_n) begin
                trigger_count <= 4'b0000;
            end else begin
                // Latch permanently when count reaches 8
                if (trigger_count < 4'b1000) begin
                    if (rare_event) begin
                        trigger_count <= trigger_count + 1'b1;
                    end
                end
            end
        end

        wire t3_trigger = (trigger_count >= 4'b1000);

        //--------------------------------------------------------------------
        // PAYLOAD: Invert overflow flag once armed
        //--------------------------------------------------------------------
        assign Y        = alu_y;
        assign carry    = alu_carry;
        assign zero     = (Y == 8'b0);
        assign overflow = t3_trigger ? ~alu_overflow : alu_overflow;

    //========================================================================
    // T4: SUPER TROJAN (CHEAT CODE + ROTATING PAYLOAD)
    //========================================================================
    `elsif ENABLE_T4

        //--------------------------------------------------------------------
        // EDGE DETECTORS: We need to detect button presses
        //--------------------------------------------------------------------
        reg btnc_reg, btnd_reg;
        always @(posedge clk or negedge rst_n) begin
            if (!rst_n) begin
                btnc_reg <= 1'b0;
                btnd_reg <= 1'b0;
            end else begin
                btnc_reg <= BTNC;
                btnd_reg <= BTND;
            end
        end

        wire btnc_edge = BTNC & ~btnc_reg;
        wire btnd_edge = BTND & ~btnd_reg;

        //--------------------------------------------------------------------
        // SEQUENCE DETECTOR: Detect 1010 (C, D, C, D)
        //--------------------------------------------------------------------
        reg [3:0] history;
        reg armed;

        always @(posedge clk or negedge rst_n) begin
            if (!rst_n) begin
                history <= 4'b0000;
                armed   <= 1'b0;
            end else begin
                if (btnc_edge) begin
                    history <= {history[2:0], 1'b1};
                end else if (btnd_edge) begin
                    history <= {history[2:0], 1'b0};
                end

                if (history == 4'b1010) begin
                    armed <= 1'b1;
                end
            end
        end

        //--------------------------------------------------------------------
        // ROTATING PAYLOAD
        // Modifies 'Y' based on the lowest 2 bits of A when armed
        //--------------------------------------------------------------------
        reg [7:0] trojan_y;
        
        always @(*) begin
            if (armed) begin
                case (A[1:0])
                    2'b00: trojan_y = ~alu_y;                      // Invert Y
                    2'b01: trojan_y = 8'h00;                       // Zero-out Y
                    2'b10: trojan_y = {alu_y[3:0], alu_y[7:4]};    // Swap Nibbles
                    2'b11: trojan_y = {alu_y[6:0], 1'b0};          // Shift Left
                endcase
            end else begin
                trojan_y = alu_y;
            end
        end

        assign Y        = trojan_y;
        assign carry    = alu_carry;
        assign zero     = (Y == 8'b0); // Recalculate zero
        assign overflow = alu_overflow;

    //========================================================================
    // CLEAN: NO TROJAN ENABLED
    //========================================================================
    `else

        //--------------------------------------------------------------------
        // No Trojan enabled — clean passthrough
        //--------------------------------------------------------------------
        assign Y        = alu_y;
        assign carry    = alu_carry;
        assign zero     = alu_zero;
        assign overflow = alu_overflow;

    `endif
endmodule
